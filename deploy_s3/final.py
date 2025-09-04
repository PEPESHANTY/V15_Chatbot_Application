# final.py — RiceAI agent with thread_id, chit-chat path, streaming (flush=True),
# SQLite checkpointing + S3 write-through for chats and SQLite backups

import os
import re
import json
import time
import sqlite3
from pathlib import Path
from typing import List, Dict, TypedDict, Any, Optional

from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

from qdrant_client import QdrantClient
from openai import OpenAI

from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_core.messages import (
    BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
)
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.tools import tool
from pydantic import BaseModel, Field

# --- Your Neo4j KG tool ---
from kg_graph_tool import ask as kg_ask

# =========================
# Env & clients
# =========================
load_dotenv()  # loads .env from CWD

# Allow .env overrides if file was read manually previously
env_path = Path(".") / ".env"
if env_path.exists():
    with env_path.open() as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ.setdefault(key, value)

QDRANT_URL = os.environ["QDRANT_URL"]
QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
COLLECTION_NAME = os.environ["QDRANT_COLLECTION_NAME"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# --- S3 config
AWS_REGION  = os.getenv("AWS_DEFAULT_REGION", "eu-north-1")
AWS_BUCKET  = os.getenv("AWS_S3_BUCKET", "riceai-chatstore")
S3_PREFIX_CHATS  = os.getenv("S3_PREFIX_CHATS", "prod/NEW/chats")
S3_PREFIX_SQLITE = os.getenv("S3_PREFIX_SQLITE", "prod/NEW/data")

# --- Local paths
Path("data").mkdir(exist_ok=True)
CHAT_DIR = Path("NEW/chats"); CHAT_DIR.mkdir(parents=True, exist_ok=True)
SQLITE_PATH = Path("data/agent_state.sqlite")

# --- Clients
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

# =========================
# S3 helpers
# =========================
def _chat_file(thread_id: str) -> Path:
    # JSONL: one record per line
    return CHAT_DIR / f"{thread_id}.jsonl"

def _s3_chat_key(thread_id: str) -> str:
    return f"{S3_PREFIX_CHATS.rstrip('/')}/{thread_id}.jsonl"

def _safe_s3_download(key: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        s3.download_file(AWS_BUCKET, key, str(dest))
        return True
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchKey", "NotFound"):
            return False
        raise

def ensure_thread_local_copy(thread_id: str) -> None:
    """Fetch chat file from S3 if local is missing."""
    lf = _chat_file(thread_id)
    if not lf.exists():
        _safe_s3_download(_s3_chat_key(thread_id), lf)

def append_chat_event(thread_id: str, role: str, content: str, meta: Dict[str, Any] | None = None) -> None:
    """Append one chat record locally and immediately sync to S3."""
    ensure_thread_local_copy(thread_id)
    rec = {
        "ts": int(time.time()),
        "role": role,         # "user" | "assistant" | "system"
        "content": content,
        "meta": meta or {},
    }
    lf = _chat_file(thread_id)
    with lf.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    # upload whole file (simple & robust)
    s3.upload_file(str(lf), AWS_BUCKET, _s3_chat_key(thread_id))

def backup_sqlite_now() -> None:
    """Upload SQLite checkpoint to S3 (idempotent)."""
    if SQLITE_PATH.exists():
        s3.upload_file(str(SQLITE_PATH), AWS_BUCKET, f"{S3_PREFIX_SQLITE.rstrip('/')}/{SQLITE_PATH.name}")

# =========================
# Helpers
# =========================
def get_query_embedding(text: str) -> List[float]:
    resp = openai_client.embeddings.create(model="text-embedding-3-small", input=text)
    return resp.data[0].embedding

def format_document_details(docs: List[Document]) -> str:
    blocks = []
    for doc in docs:
        meta = doc.metadata or {}
        blocks.append(
            f"- **Title:** {meta.get('title', 'No title')} (score: {meta.get('score', 0):.3f})  \n"
            f"  **URL:** {meta.get('url', 'N/A')}  \n"
            f"  **Source:** {meta.get('source', 'N/A')}  \n"
            f"  **Summary:** {meta.get('summary', '')[:150]}...  \n"
            f"  **Preview:** {doc.page_content[:150]}...  \n"
        )
    return "\n".join(blocks) if blocks else "_No sources found._"

def build_memory_system_prompt(user_facts: Dict[str, str]) -> str:
    if not user_facts:
        return "Known user facts: (none). Do not invent facts. Be friendly and concise."
    parts = [f"- {k}: {v}" for k, v in user_facts.items() if str(v).strip()]
    return "Known user facts:\n" + "\n".join(parts)

# -------- intent & ag-question heuristics (less sensitive) --------
QUESTION_CUE_PAT = re.compile(
    r"\b(what|how|when|where|why|which|should|can|could|would|advise|recommend|rate|"
    r"calculate|compare|best|steps|practice|guide|help|list|tell me)\b|\?",
    re.I,
)

AG_TOKENS = (
    r"rice|paddy|variet|seed|nursery|transplant|sow|broadcast|yield|"
    r"fertiliz|urea|dap|npk|kcl|organic|compost|manure|"
    r"aw[dt]|irrigat|drain|flood|water|soil|"
    r"ipm|pest|insect|weed|herbicide|fungicide|pesticide|disease|blast|bph|"
    r"harvest|dry|mill|straw|residue|mrl|ban list|regulation"
)
AG_PAT = re.compile(rf"\b(?:{AG_TOKENS})\b", re.I)

GREET_PAT = re.compile(r"\b(hi|hello|hey|good\s+(morning|afternoon|evening))\b", re.I)
SELF_INFO_PAT = re.compile(
    r"\b(i\s*(?:am|'m|study|studying|work|working|live|living|from|in|at)|"
    r"my\s*(?:name|college|university|job|profession|location)\b)",
    re.I,
)

def _looks_like_ag_question(text: str) -> bool:
    """Return True only when it's clearly an agriculture *question*."""
    t = (text or "").strip().lower()
    if not QUESTION_CUE_PAT.search(t):
        return False
    ag_hits = re.findall(AG_PAT, t)
    return ("rice" in t) or (len(ag_hits) >= 2)

def _is_self_info_or_greeting(text: str) -> bool:
    t = (text or "").strip()
    return bool(GREET_PAT.search(t) or SELF_INFO_PAT.search(t))

# =========================
# Tools (Qdrant + Neo4j KG)
# =========================
@tool(
    "qdrant_search",
    return_direct=False,
    description="Vector-search Qdrant for relevant rice/ag documents. Args: query, k, threshold. Returns: {'hits':[...]}."
)
def qdrant_search(query: str, k: int = 5, threshold: float = 0.35) -> Dict[str, Any]:
    """Vector-search Qdrant for rice/ag documents."""
    print(f"[tool:qdrant_search] query='{query}', k={k}, threshold={threshold}")
    emb = get_query_embedding(query)
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=emb,
        limit=k,
        with_payload=True,
        with_vectors=False,
        score_threshold=threshold,
    )
    hits = []
    for r in results:
        payload = r.payload or {}
        hits.append({
            "score": r.score,
            "content": payload.get("content", ""),
            "title": payload.get("title", ""),
            "summary": payload.get("summary", ""),
            "url": payload.get("url", ""),
            "source": payload.get("source", ""),
            "chunk_id": payload.get("chunk_id", ""),
        })
    print(f"[tool:qdrant_search] returned {len(hits)} hits")
    return {"hits": hits}

@tool(
    "neo4j_kg_search",
    return_direct=False,
    description="Query the Neo4j knowledge graph and return a grounded answer with facts. Args: query, limit. Returns: {'hits':[...]}."
)
def neo4j_kg_search(query: str, limit: int = 5) -> Dict[str, Any]:
    """Query Neo4j knowledge graph for grounded answers and facts."""
    print(f"[tool:neo4j_kg_search] query='{query}', limit={limit}")
    from math import isfinite
    KG_MAX_DISTANCE = float(os.getenv("KG_MAX_DISTANCE", "0.85"))

    kg_res = kg_ask(query, chapter=None, top_k=limit, expand=min(4, max(1, limit)), per_node_limit=25)
    kg_hits = kg_res.get("hits", []) or []
    if not kg_hits:
        print("[tool:neo4j_kg_search] no KG hits")
        return {"hits": []}

    try:
        top_dist = float(kg_hits[0].get("score", 1.0))
    except Exception:
        top_dist = 1.0

    if not isfinite(top_dist) or top_dist > KG_MAX_DISTANCE:
        print(f"[tool:neo4j_kg_search] top distance {top_dist:.4f} > threshold {KG_MAX_DISTANCE:.4f} -> ignore KG")
        return {"hits": []}

    sim = max(0.0, min(1.0, 1.0 - top_dist))
    top = kg_hits[0]
    top_id   = top.get("id", "KG")
    top_name = top.get("name", top_id)
    answer   = (kg_res.get("answer") or "").strip()

    main_hit = {
        "score": sim,
        "content": answer,
        "title": f"Knowledge Graph: {top_name}",
        "summary": "Grounded answer from the Neo4j knowledge graph (with citations).",
        "url": "",
        "source": "neo4j-kg",
        "chunk_id": f"kg_{top_id}",
    }

    fact_hits = []
    for i, f in enumerate(kg_res.get("facts", [])[: max(0, limit - 1)]):
        fact_hits.append({
            "score": round(sim * 0.9, 6),
            "content": f.get("text", ""),
            "title": "KG Fact",
            "summary": "",
            "url": "",
            "source": "neo4j-kg",
            "chunk_id": f"kg_fact_{top_id}_{i}",
        })

    out = {"hits": [main_hit] + fact_hits}
    print(f"[tool:neo4j_kg_search] returning {len(out['hits'])} hits (sim={sim:.4f}, dist={top_dist:.4f})")
    return out

TOOLS = [qdrant_search, neo4j_kg_search]

def _clean_msgs_for_llm(msgs: List[BaseMessage]) -> List[BaseMessage]:
    return [m for m in msgs if not isinstance(m, ToolMessage)]

def _summarize_msgs_for_prompt(msgs: List[BaseMessage]) -> str:
    lines = []
    for m in msgs[-8:]:
        if isinstance(m, HumanMessage):
            lines.append(f"User: {m.content}")
        elif isinstance(m, AIMessage):
            lines.append(f"Assistant: {m.content}")
    return "\n".join(lines)

# =========================
# Prompts & LLMs
# =========================
rewriter_system = SystemMessage(content=(
    "Rewrite the user's latest message as a single, standalone query optimized for retrieval.\n"
    "Preserve key entities (e.g., Vietnam, Mekong Delta), inputs (crop stage/soil), and regulatory intent.\n"
    "Prefer adding clarifying terms like 'rice', 'agriculture', 'IPM', 'MRL', 'ban list', 'regulation' when implied.\n"
    "Return ONLY the refined query."
))

planner_system = SystemMessage(content=(
    "You are a retrieval planner. Decide which tools to call to fetch context.\n"
    "- Use qdrant_search for semantic docs.\n"
    "- If the question mentions practices/entities/relationships (AWD, straw, IPM, mechanization) ALSO call neo4j_kg_search.\n"
    "- When unsure: call BOTH (qdrant first). Keep calls minimal but sufficient."
))

rag_template = """
You are RiceAI Expert, a trusted agronomist trained on sustainable, high-yield rice practices.

{memory_system}

INSTRUCTIONS:
- Answer using the retrieved context. If conflicts, state the most reliable practice and note uncertainty.
- Be explicit, practical, and step-by-step.
- Include actionable numbers (rates, timings) when available.

Chat history (may help for continuity): {history}

Retrieved context:
{context}

User question: {question}
"""
rag_prompt = ChatPromptTemplate.from_template(rag_template)

chitchat_base = (
    "You are a warm, concise assistant. Keep replies brief and friendly. "
    "Use known user facts naturally. If you don't know a fact, don't guess—invite the user to share it."
)

rag_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)
planner_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).bind_tools(TOOLS)
chitchat_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, openai_api_key=OPENAI_API_KEY)
rewriter_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)

rag_chain = rag_prompt | rag_llm

# =========================
# State + Schemas
# =========================
class AgentState(TypedDict):
    messages: List[BaseMessage]
    documents: List[Document]
    label: str                    # 'rice', 'chitchat', 'offtopic'
    rephrased_question: str
    proceed_to_generate: bool
    rephrase_count: int
    question: HumanMessage
    user_facts: Dict[str, str]

class GradeLabel(BaseModel):
    label: str = Field(..., description="One of: rice, chitchat, offtopic")

class GradeDocument(BaseModel):
    score: str = Field(..., description="Respond with 'Yes' or 'No'")

# =========================
# Nodes
# =========================
def question_rewriter(state: AgentState) -> AgentState:
    print("=== Entering question_rewriter ===")

    # ---- normalize state WITHOUT setdefault ----
    # user_facts -> dict
    if not isinstance(state.get("user_facts"), dict):
        state["user_facts"] = {}
    # messages -> list
    msgs = state.get("messages")
    if not isinstance(msgs, list):
        msgs = []
    state["messages"] = msgs
    # rephrase_count -> int
    rc = state.get("rephrase_count")
    if not isinstance(rc, int):
        rc = 0
    state["rephrase_count"] = rc

    # ---- read question & append safely ----
    q_msg = state.get("question")
    if isinstance(q_msg, HumanMessage):
        q = q_msg.content or ""
        # only append if last human content differs
        if not state["messages"] or not (
            isinstance(state["messages"][-1], HumanMessage)
            and state["messages"][-1].content == q
        ):
            state["messages"].append(q_msg)
    elif isinstance(q_msg, BaseMessage):
        q = q_msg.content or ""
        state["messages"].append(q_msg)
    elif isinstance(q_msg, str):
        q = q_msg
        state["messages"].append(HumanMessage(content=q))
    else:
        q = ""

    # default to original
    state["rephrased_question"] = q

    # small-talk/greeting? keep original, skip rewriting
    if _is_self_info_or_greeting(q) or (len(q.split()) <= 4 and not _looks_like_ag_question(q)):
        print("[question_rewriter] small-talk -> keep original")
        return state

    # include recent context (strip tool messages)
    conversation = _clean_msgs_for_llm(state["messages"][:-1]) if len(state["messages"]) > 1 else []

    rewriter_system_local = SystemMessage(content=(
        "Rewrite the user's latest message as a single, standalone query optimized for retrieval. "
        "Preserve key entities (e.g., Vietnam, Mekong Delta), crop/soil/stage details, and any regulatory intent. "
        "When implied, add clarifiers like 'rice', 'agriculture', 'IPM', 'MRL', 'ban list', 'regulation'. "
        "Return ONLY the refined query."
    ))

    try:
        resp = rewriter_llm.invoke([rewriter_system_local, *conversation, HumanMessage(content=q or "N/A")])
        refined = (resp.content or "").strip()
        if refined:
            state["rephrased_question"] = refined
            print(f"[question_rewriter] Rephrased: {refined}")
        else:
            print("[question_rewriter] Empty rewrite; using original.")
    except Exception as e:
        print(f"[question_rewriter] Rewrite failed: {e}; using original.")

    return state


def fact_extractor(state: AgentState) -> AgentState:
    print("=== Entering fact_extractor (LLM memory) ===")
    state.setdefault("user_facts", {})
    latest = state["question"].content

    # LLM-first extraction (JSON only)
    system = SystemMessage(content=(
        "From the user's last message, extract stable personal facts as a *compact JSON object*.\n"
        "Allowed keys: name, location, city, country, residence, profession, college, farm_size, rice_variety, "
        "role, company, preferences, email, phone, other.\n"
        "Return ONLY JSON. If none, return {}."
    ))
    human = HumanMessage(content=latest)
    data: Dict[str, str] = {}
    try:
        resp = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).invoke([system, human])
        txt = (resp.content or "").strip()
        if txt.startswith("{"):
            data = json.loads(txt)
    except Exception:
        data = {}

    # Heuristic fallback from raw text
    if not data.get("location"):
        m = re.search(r"\b(?:i\s*(?:am|'m)?\s*(?:from|in)|i\s*live\s*in|living\s*in|reside\s*in)\s+([A-Za-z .,'-]+)", latest, re.I)
        if m:
            loc = m.group(1).strip(" .,'-")
            if loc:
                data["location"] = loc
    if not data.get("name"):
        m = re.search(r"\b(?:my\s*name\s*is|i\s*am|i'm)\s+([A-Za-z][A-Za-z .'-]{1,40})\b", latest.strip(), re.I)
        if m:
            data["name"] = m.group(1).strip(" .,'-")
    if not data.get("college"):
        m = re.search(r"\b(?:study|studying|student)\s+(?:at\s+)?([A-Za-z][A-Za-z .&'-]{1,80})\b", latest, re.I)
        if m:
            data["college"] = m.group(1).strip(" .,'-")

    if isinstance(data, dict):
        cleaned = {k: str(v).strip() for k, v in data.items() if str(v).strip()}
        if cleaned:
            state["user_facts"].update(cleaned)
            print(f"[fact_extractor] user_facts = {state['user_facts']}")
    return state

def question_classifier(state: AgentState) -> AgentState:
    print("=== Entering question_classifier ===")
    q = state.get("rephrased_question", "") or state.get("question", HumanMessage(content="")).content

    # If it's clearly self-info or greeting -> chit-chat path
    if _is_self_info_or_greeting(q):
        state["label"] = "chitchat"
        print("[question_classifier] self-info/greeting -> chitchat")
        return state

    # Strict ag-question heuristic
    if _looks_like_ag_question(q):
        state["label"] = "rice"
        print("[question_classifier] heuristics -> rice")
        return state

    # LLM fallback (bias toward chit-chat)
    system_message = SystemMessage(
        content=(
            "Classify the user's message into one label.\n"
            "Use 'rice' only if they are *asking* for agriculture/rice information or advice "
            "(AWD, IPM, fertilizer, pests, water, soils, varieties, harvest, markets, MRLs, etc.).\n"
            "'chitchat' covers greetings, small talk, or when the user is simply sharing personal information "
            "(name, location, college, job) without requesting advice.\n"
            "'offtopic' is unrelated.\n"
            "If uncertain, choose 'chitchat'."
        )
    )
    human_message = HumanMessage(content=f"User message: {q}\nLabel (rice|chitchat|offtopic):")
    grade_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    grader_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).with_structured_output(GradeLabel)
    result = (grade_prompt | grader_llm).invoke({})
    state["label"] = result.label.strip().lower()
    print(f"[question_classifier] label = {state['label']}")
    return state

def retrieve_planner(state: AgentState) -> AgentState:
    print("=== Entering retrieve_planner ===")
    question = state["rephrased_question"]
    messages = [planner_system, HumanMessage(content=f"Plan retrieval for: {question}")]
    ai = planner_llm.invoke(messages)
    state.setdefault("messages", [])
    state["messages"].append(ai)
    print(f"[retrieve_planner] Tool calls planned: {getattr(ai, 'tool_calls', [])}")
    return state

tool_node = ToolNode(TOOLS)

def collect_tool_results(state: AgentState) -> AgentState:
    print("=== Entering collect_tool_results ===")
    tool_msgs = [m for m in state["messages"] if isinstance(m, ToolMessage)]
    hits_all: List[Dict[str, Any]] = []
    for tm in tool_msgs:
        payload: Dict[str, Any] = {}
        if isinstance(tm.content, str):
            try:
                payload = json.loads(tm.content)
            except Exception:
                payload = {}
        elif isinstance(tm.content, dict):
            payload = tm.content
        hits_all.extend(payload.get("hits", []))

    best_by_chunk: Dict[str, Dict[str, Any]] = {}
    for h in hits_all:
        cid = h.get("chunk_id") or f"row_{len(best_by_chunk)}"
        if cid not in best_by_chunk or h.get("score", 0) > best_by_chunk[cid].get("score", 0):
            best_by_chunk[cid] = h
    ordered = sorted(
        best_by_chunk.values(),
        key=lambda x: x.get("score", 0) if not isinstance(x.get("score"), str) else float(x.get("score") or 0),
        reverse=True
    )

    docs: List[Document] = []
    for h in ordered:
        docs.append(Document(
            page_content=h.get("content", ""),
            metadata={
                "score": h.get("score", 0.0),
                "title": h.get("title", ""),
                "summary": h.get("summary", ""),
                "url": h.get("url", ""),
                "source": h.get("source", ""),
                "chunk_id": h.get("chunk_id", ""),
            }
        ))
    state["documents"] = docs
    print(f"[collect_tool_results] Collected {len(docs)} documents")
    return state

class GradeDocument(BaseModel):
    score: str = Field(..., description="Yes or No")

def retrieval_grader(state: AgentState) -> AgentState:
    print("=== Entering retrieval_grader ===")
    relevant_docs: List[Document] = []
    for doc in state["documents"]:
        system_message = SystemMessage(content="You are a grader assessing relevance. Reply 'Yes' or 'No'.")
        human_message = HumanMessage(content=f"User question: {state['rephrased_question']}\n\nRetrieved:\n{doc.page_content}")
        grade_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
        grader_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).with_structured_output(GradeDocument)
        result = (grade_prompt | grader_llm).invoke({})
        print(f"[retrieval_grader] Doc preview: {doc.page_content[:30]!r} -> {result.score.strip()}")
        if result.score.strip().lower() == "yes":
            relevant_docs.append(doc)
    state["documents"] = relevant_docs
    state["proceed_to_generate"] = len(relevant_docs) > 0
    print(f"[retrieval_grader] proceed_to_generate = {state['proceed_to_generate']} (kept {len(relevant_docs)})")
    return state

def proceed_router(state: AgentState) -> str:
    print("=== Entering proceed_router ===")
    if state.get("proceed_to_generate", False):
        print("[proceed_router] -> generate_answer")
        return "generate_answer"
    elif state.get("rephrase_count", 0) >= 2:
        print("[proceed_router] -> cannot_answer")
        return "cannot_answer"
    else:
        print("[proceed_router] -> refine_question")
        return "refine_question"

def refine_question(state: AgentState) -> AgentState:
    print("=== Entering refine_question ===")
    if state.get("rephrase_count", 0) >= 2:
        return state
    q = state["rephrased_question"]

    # If it doesn't look like an ag question, stop refining (prevents loops on self-info)
    if not _looks_like_ag_question(q):
        print("[refine_question] not an ag question -> stop refining")
        state["rephrase_count"] = 2
        return state

    rewriter_system2 = SystemMessage(content=(
        "Rewrite the user's latest message as a single, standalone query optimized for retrieval. "
        "Preserve key entities and constraints. Return ONLY the refined query."
    ))
    human_message = HumanMessage(content=f"Original question: {q}\n\nProvide a refined standalone question only.")
    refine_prompt = ChatPromptTemplate.from_messages([rewriter_system2, human_message])
    resp = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).invoke(refine_prompt.format())
    refined = resp.content.strip()
    print(f"[refine_question] Refined: {refined}")
    state["rephrased_question"] = refined
    state["rephrase_count"] = state.get("rephrase_count", 0) + 1
    return state

def generate_answer(state: AgentState) -> AgentState:
    print("=== Entering generate_answer ===")
    history = state.get("messages", [])
    documents = state.get("documents", [])
    rq = state.get("rephrased_question", "")
    context_str = "\n\n".join(doc.page_content for doc in documents)
    memory_system = build_memory_system_prompt(state.get("user_facts", {}))

    response = rag_chain.invoke({
        "history": _summarize_msgs_for_prompt(history),
        "context": context_str,
        "question": rq,
        "memory_system": memory_system,
    })
    generation = response.content.strip()

    name = state.get("user_facts", {}).get("name")
    if name:
        generation = f"{generation}\n\n— Hope that helps, {name}!"

    sources_md = format_document_details(documents)
    final_text = f"{generation}\n\n---\n### Sources used\n{sources_md}"

    state.setdefault("messages", [])
    state["messages"].append(AIMessage(content=final_text))
    print("[generate_answer] Done. (Answer + sources appended to state['messages'])")
    return state

def answer_from_recent_context(state: AgentState, question: str) -> Optional[str]:
    ctx = "\n".join(state.get("recent_context", [])[-12:])
    if not ctx.strip():
        return None
    sys = SystemMessage(content=(
        "You will answer ONLY using the snippets below from recent turns. "
        "If the answer is not directly implied, reply exactly with NO_ANSWER."
        "\n\nSnippets:\n" + ctx
    ))
    resp = chitchat_llm.invoke([sys, HumanMessage(content=question)])
    text = (resp.content or "").strip()
    if text.upper().startswith("NO_ANSWER") or len(text) == 0:
        return None
    return text


def chit_chat(state: AgentState) -> AgentState:
    print("=== Entering chit_chat ===")

    # normalize
    if not isinstance(state.get("messages"), list):
        state["messages"] = []
    facts = state.get("user_facts", {}) or {}

    # read user question safely
    q_obj = state.get("question")
    q = q_obj.content if hasattr(q_obj, "content") else (q_obj or "")
    q = (q or "").strip()
    qlow = q.lower()

    # ---------- 1) try answering purely from recent_context ----------
    try:
        recent_ans = answer_from_recent_context(state, q)  # your helper
    except NameError:
        recent_ans = None
    if recent_ans:
        state["messages"].append(AIMessage(content=recent_ans))
        return state

    # ---------- 2) specific easy asks ----------
    if re.search(r"\b(what'?s|what is)\s+my\s+name\b|\bwho\s+am\s+i\b", qlow):
        name = (facts.get("name") or "").strip()
        text = f"You told me your name is **{name}**." if name else \
               "I don't have your name yet—what should I call you?"
        state["messages"].append(AIMessage(content=text))
        return state

    if re.search(r"\bwhere\s+do\s+i\s+live\b|\bwhere\s+am\s+i\s+from\b|\bmy\s+current\s+place\b|\bwhere\s+i\s+live\b", qlow):
        loc = (facts.get("location") or facts.get("city") or facts.get("country") or facts.get("residence") or "").strip()
        text = f"You told me you live in **{loc}**." if loc else \
               "I don't have your location yet—where do you live?"
        state["messages"].append(AIMessage(content=text))
        return state

    # ---------- 3) “what do you know about me?” -> list everything we have ----------
    if re.search(r"what\s+(all\s+)?do\s+you\s+know\s+about\s+me|tell\s+me\s+about\s+myself|what\s+do\s+you\s+remember\s+about\s+me", qlow):
        nonempty = {k: v for k, v in facts.items() if str(v).strip()}
        if nonempty:
            lines = []
            for k, v in nonempty.items():
                label = "sports you play" if k.lower() == "sports" else k.replace("_", " ")
                lines.append(f"- **{label}**: {v}")
            text = "Here’s what I know so far:\n" + "\n".join(lines)
        else:
            text = "I only know a little so far. Share more and I’ll remember it."
        state["messages"].append(AIMessage(content=text))
        return state

    # ---------- 4) generic: “what is my <anything>?” / “do you know my <anything>?” ----------
    m = re.search(r"(?:what(?:'s| is| are)?\s+my\s+|do\s+you\s+know\s+my\s+)([a-z0-9 _\-]{2,60})\??", qlow)
    if m and isinstance(facts, dict) and facts:
        asked = m.group(1).strip()

        def norm(s: str) -> str:
            return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

        asked_n = norm(asked)
        best_key, best_val = None, ""
        # try direct/containment match against ANY key in user_facts
        for k, v in facts.items():
            if not str(v).strip():
                continue
            k_n = norm(k)
            if not k_n:
                continue
            if k_n == asked_n or k_n in asked_n or asked_n in k_n:
                best_key, best_val = k, str(v).strip()
                break
            # token overlap heuristic
            if any(tok and tok in k_n for tok in asked_n.split()):
                best_key, best_val = k, str(v).strip()
                break

        if best_key and best_val:
            label = best_key.replace("_", " ")
            text = f"Your **{label}** is **{best_val}**."
            state["messages"].append(AIMessage(content=text))
            return state

    # ---------- 5) friendly fallback with memory context ----------
    mem_line = build_memory_system_prompt(facts)
    system = SystemMessage(content=f"{chitchat_base}\n\n{mem_line}\nWhen it's natural, weave one relevant fact into the reply.")
    resp = chitchat_llm.invoke([system, HumanMessage(content=q)])
    text = (resp.content or "").strip()

    state["messages"].append(AIMessage(content=text))
    return state


def cannot_answer(state: AgentState) -> AgentState:
    print("=== Entering cannot_answer ===")
    state.setdefault("messages", [])
    state["messages"].append(AIMessage(content="I'm sorry, but I couldn't find enough information to answer that clearly."))
    return state

def off_topic_response(state: AgentState) -> AgentState:
    print("=== Entering off_topic_response ===")
    state.setdefault("messages", [])
    state["messages"].append(AIMessage(content="I'm focused on rice farming topics. Ask me about cultivation, water, fertilizer, IPM, AWD, harvest, markets, etc."))
    return state

# =========================
# Graph
# =========================
workflow = StateGraph(AgentState)

workflow.add_node("question_rewriter", question_rewriter)
workflow.add_node("fact_extractor", fact_extractor)
workflow.add_node("question_classifier", question_classifier)
workflow.add_node("retrieve_planner", retrieve_planner)
workflow.add_node("tools", tool_node)
workflow.add_node("collect_tool_results", collect_tool_results)
workflow.add_node("retrieval_grader", retrieval_grader)
workflow.add_node("generate_answer", generate_answer)
workflow.add_node("refine_question", refine_question)
workflow.add_node("cannot_answer", cannot_answer)
workflow.add_node("off_topic_response", off_topic_response)
workflow.add_node("chit_chat", chit_chat)

workflow.add_edge("question_rewriter", "fact_extractor")
workflow.add_edge("fact_extractor", "question_classifier")

workflow.add_conditional_edges(
    "question_classifier",
    lambda s: "retrieve_planner" if s.get("label") == "rice" else ("chit_chat" if s.get("label") == "chitchat" else "off_topic_response"),
    {
        "retrieve_planner": "retrieve_planner",
        "chit_chat": "chit_chat",
        "off_topic_response": "off_topic_response",
    },
)

workflow.add_edge("retrieve_planner", "tools")
workflow.add_edge("tools", "collect_tool_results")
workflow.add_edge("collect_tool_results", "retrieval_grader")

workflow.add_conditional_edges(
    "retrieval_grader",
    lambda s: "generate_answer" if s.get("proceed_to_generate") else ("cannot_answer" if s.get("rephrase_count", 0) >= 2 else "refine_question"),
    {
        "generate_answer": "generate_answer",
        "refine_question": "refine_question",
        "cannot_answer": "cannot_answer",
    },
)
workflow.add_edge("refine_question", "retrieve_planner")

workflow.add_edge("generate_answer", END)
workflow.add_edge("cannot_answer", END)
workflow.add_edge("off_topic_response", END)
workflow.add_edge("chit_chat", END)

# =========================
# Compile with SQLite checkpointer (per thread)
# =========================
workflow.set_entry_point("question_rewriter")

conn = sqlite3.connect(str(SQLITE_PATH), check_same_thread=False)
checkpointer = SqliteSaver(conn)
graph = workflow.compile(checkpointer=checkpointer)

# =========================
# Streaming helpers
# =========================
def stream_answer(question: str, thread_id: Any):
    input_data = {"question": HumanMessage(content=question)}
    last_printed = ""

    for state_update in graph.stream(
        input=input_data,
        config={"configurable": {"thread_id": thread_id}},
        stream_mode="values",
        flush=True,
    ):
        msgs: Optional[List[BaseMessage]] = state_update.get("messages") if isinstance(state_update, dict) else None
        if not msgs:
            continue
        ai_msgs = [m for m in msgs if isinstance(m, AIMessage)]
        if not ai_msgs:
            continue
        content = ai_msgs[-1].content
        if not isinstance(content, str):
            continue
        if len(content) > len(last_printed) and content.startswith(last_printed):
            delta = content[len(last_printed):]
            last_printed = content
            if delta:
                yield delta
        else:
            last_printed = content
            yield content

# =========================
# CLI loop
# =========================
if __name__ == "__main__":
    print("RiceAI Agent — type '/new' for a fresh thread, '/stream' to toggle streaming, 'quit' to exit.")
    thread_id = "default-thread"
    streaming = False

    # If you resume an existing thread_id, pull prior chat file (no-op if new)
    ensure_thread_local_copy(thread_id)

    while True:
        user_q = input("You: ").strip()
        if user_q.lower() in {"quit", "exit"}:
            break
        if user_q.lower() == "/new":
            import uuid
            thread_id = str(uuid.uuid4())
            ensure_thread_local_copy(thread_id)
            print(f"[system] New thread_id = {thread_id}")
            continue
        if user_q.lower() == "/stream":
            streaming = not streaming
            print(f"[system] Streaming is now {'ON' if streaming else 'OFF'}")
            continue

        input_data = {"question": HumanMessage(content=user_q)}

        # Log user question immediately
        append_chat_event(thread_id, "user", user_q)

        if streaming:
            print("Assistant: ", end="", flush=True)
            full = ""
            for piece in stream_answer(user_q, thread_id):
                full += piece
                print(piece, end="", flush=True)
            print("\n" + "-" * 40)
            append_chat_event(thread_id, "assistant", full)
            backup_sqlite_now()
        else:
            result = graph.invoke(input=input_data, config={"configurable": {"thread_id": thread_id}})
            if "messages" in result and result["messages"]:
                replies = [m for m in result["messages"] if isinstance(m, AIMessage)]
                if replies:
                    answer = replies[-1].content
                    print("\nAssistant:\n" + answer)
                    append_chat_event(thread_id, "assistant", answer)
                    backup_sqlite_now()
                else:
                    print("\nAssistant: (no AI reply)")
            else:
                print("\nAssistant: (no response)")
            print("-" * 40)
