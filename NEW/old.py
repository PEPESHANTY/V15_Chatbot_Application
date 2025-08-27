
# # final.py — RiceAI agent with thread_id, chit-chat path, and LangGraph streaming (flush=True)
#
# import os
# from pathlib import Path
# from typing import List, Dict, TypedDict, Any, Optional
#
# from dotenv import load_dotenv
# from qdrant_client import QdrantClient
# from openai import OpenAI
#
# from langchain.schema import Document
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langgraph.graph import StateGraph, END
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.prebuilt import ToolNode
# from langchain_core.messages import (
#     BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
# )
# from langchain.tools import tool
# from pydantic import BaseModel, Field
#
# # --- KG query tool you already have ---
# from kg_graph_tool import ask as kg_ask
#
# # =========================
# # Env & clients
# # =========================
# load_dotenv()
# env_path = Path('.') / '.env'
# if env_path.exists():
#     with open(env_path) as f:
#         for line in f:
#             if '=' in line and not line.strip().startswith('#'):
#                 key, value = line.strip().split('=', 1)
#                 os.environ.setdefault(key, value)
#
# QDRANT_URL = os.environ["QDRANT_URL"]
# QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]
# COLLECTION_NAME = os.environ["QDRANT_COLLECTION_NAME"]
# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
#
# qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
# openai_client = OpenAI(api_key=OPENAI_API_KEY)
#
# # =========================
# # Helpers
# # =========================
# def get_query_embedding(text: str) -> List[float]:
#     resp = openai_client.embeddings.create(model="text-embedding-3-small", input=text)
#     return resp.data[0].embedding
#
# def format_document_details(docs: List[Document]) -> str:
#     blocks = []
#     for doc in docs:
#         meta = doc.metadata or {}
#         blocks.append(
#             f"- Title: {meta.get('title', 'No title')} (score: {meta.get('score', 0):.3f})\n"
#             f"  URL: {meta.get('url', 'N/A')}\n"
#             f"  Source: {meta.get('source', 'N/A')}\n"
#             f"  Summary: {meta.get('summary', '')[:150]}...\n"
#             f"  Preview: {doc.page_content[:150]}...\n"
#         )
#     return "\n".join(blocks) if blocks else "_No sources found._"
#
# # =========================
# # Tools (Qdrant + Neo4j KG)
# # =========================
# @tool("qdrant_search", return_direct=False)
# def qdrant_search(query: str, k: int = 5, threshold: float = 0.35) -> Dict[str, Any]:
#     """
#     Vector search over Qdrant.
#     """
#     print(f"[tool:qdrant_search] query='{query}', k={k}, threshold={threshold}")
#     emb = get_query_embedding(query)
#     results = qdrant.search(
#         collection_name=COLLECTION_NAME,
#         query_vector=emb,
#         limit=k,
#         with_payload=True,
#         with_vectors=False,
#         score_threshold=threshold
#     )
#     hits = []
#     for r in results:
#         payload = r.payload or {}
#         hits.append({
#             "score": r.score,
#             "content": payload.get("content", ""),
#             "title": payload.get("title", ""),
#             "summary": payload.get("summary", ""),
#             "url": payload.get("url", ""),
#             "source": payload.get("source", ""),
#             "chunk_id": payload.get("chunk_id", "")
#         })
#     print(f"[tool:qdrant_search] returned {len(hits)} hits")
#     return {"hits": hits}
#
# @tool("neo4j_kg_search", return_direct=False)
# def neo4j_kg_search(query: str, limit: int = 5) -> Dict[str, Any]:
#     """
#     Neo4j KG search -> formatted grounded answer + a few facts.
#     Only returns hits if top distance <= KG_MAX_DISTANCE.
#     """
#     print(f"[tool:neo4j_kg_search] query='{query}', limit={limit}")
#     from math import isfinite
#     KG_MAX_DISTANCE = float(os.getenv("KG_MAX_DISTANCE", "0.85"))
#
#     kg_res = kg_ask(query, chapter=None, top_k=limit, expand=min(4, max(1, limit)), per_node_limit=25)
#     kg_hits = kg_res.get("hits", []) or []
#     if not kg_hits:
#         print("[tool:neo4j_kg_search] no KG hits")
#         return {"hits": []}
#
#     try:
#         top_dist = float(kg_hits[0].get("score", 1.0))
#     except Exception:
#         top_dist = 1.0
#
#     if not isfinite(top_dist) or top_dist > KG_MAX_DISTANCE:
#         print(f"[tool:neo4j_kg_search] top distance {top_dist:.4f} > threshold {KG_MAX_DISTANCE:.4f} -> ignore KG")
#         return {"hits": []}
#
#     sim = max(0.0, min(1.0, 1.0 - top_dist))
#     top = kg_hits[0]
#     top_id   = top.get("id", "KG")
#     top_name = top.get("name", top_id)
#     answer   = (kg_res.get("answer") or "").strip()
#
#     main_hit = {
#         "score": sim,
#         "content": answer,
#         "title": f"Knowledge Graph: {top_name}",
#         "summary": "Grounded answer from the Neo4j knowledge graph (with citations).",
#         "url": "",
#         "source": "neo4j-kg",
#         "chunk_id": f"kg_{top_id}",
#     }
#
#     fact_hits = []
#     for i, f in enumerate(kg_res.get("facts", [])[: max(0, limit - 1)]):
#         fact_hits.append({
#             "score": round(sim * 0.9, 6),
#             "content": f.get("text", ""),
#             "title": "KG Fact",
#             "summary": "",
#             "url": "",
#             "source": "neo4j-kg",
#             "chunk_id": f"kg_fact_{top_id}_{i}",
#         })
#
#     out = {"hits": [main_hit] + fact_hits}
#     print(f"[tool:neo4j_kg_search] returning {len(out['hits'])} hits (sim={sim:.4f}, dist={top_dist:.4f})")
#     return out
#
# TOOLS = [qdrant_search, neo4j_kg_search]
#
# # =========================
# # LLMs and prompts
# # =========================
# rag_template = """
# You are RiceAI Expert, a trusted agronomist and AI agent trained on sustainable and high-yield rice farming practices.
#
# When answering the question, use all relevant context provided. Explain the answer thoroughly and cover all key details, so that no important information is omitted. Be explicit and comprehensive.
#
# Chat history: {history}
#
# Retrieved context: {context}
#
# Question: {question}
# """
# rag_prompt = ChatPromptTemplate.from_template(rag_template)
# rag_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)
# rag_chain = rag_prompt | rag_llm
#
# # Planner LLM (decides which tools to call)
# planner_system = SystemMessage(content=(
#     "You are a retrieval planner. Decide which tools to call to fetch context for the user's question.\n"
#     "- If the question requires semantic document retrieval, call qdrant_search.\n"
#     "- If the question mentions entities, relationships, 'chapter', practices (AWD, straw, IPM, mechanization, etc.), "
#     "  or anything structural, ALSO call neo4j_kg_search.\n"
#     "- When in doubt, call BOTH qdrant_search first and then neo4j_kg_search.\n"
#     "Keep calls minimal but sufficient."
# ))
# planner_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).bind_tools(TOOLS)
#
# # Chit-chat LLM (friendly, brief)
# chitchat_system = SystemMessage(content=(
#     "You are a friendly assistant. Keep answers brief and conversational. "
#     "If the user asks for their name, say you don't actually know but you're happy to use any name they prefer."
# ))
# chitchat_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, openai_api_key=OPENAI_API_KEY)
#
# # =========================
# # State + Schemas
# # =========================
# class AgentState(TypedDict):
#     messages: List[BaseMessage]
#     documents: List[Document]
#     label: str                    # 'rice', 'chitchat', 'offtopic'
#     rephrased_question: str
#     proceed_to_generate: bool
#     rephrase_count: int
#     question: HumanMessage
#
# class GradeLabel(BaseModel):
#     label: str = Field(..., description="One of: rice, chitchat, offtopic")
#
# class GradeDocument(BaseModel):
#     score: str = Field(..., description="Respond with 'Yes' or 'No'")
#
# # =========================
# # Nodes
# # =========================
# def question_rewriter(state: AgentState) -> AgentState:
#     print("=== Entering question_rewriter ===")
#     state["documents"] = []
#     state["label"] = ""
#     state["rephrased_question"] = ""
#     state["proceed_to_generate"] = False
#     state["rephrase_count"] = 0
#
#     state.setdefault("messages", [])
#     if state["question"] not in state["messages"]:
#         state["messages"].append(state["question"])
#
#     if len(state["messages"]) > 1:
#         conversation = state["messages"][:-1]
#         current_question = state["question"].content
#         msgs: List[BaseMessage] = [
#             SystemMessage(content="Rephrase the user's last message as a standalone query optimized for retrieval.")
#         ]
#         msgs.extend(conversation)
#         msgs.append(HumanMessage(content=current_question))
#         rephrase_prompt = ChatPromptTemplate.from_messages(msgs)
#         resp = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).invoke(
#             rephrase_prompt.format()
#         )
#         better = resp.content.strip()
#         print(f"[question_rewriter] Rephrased: {better}")
#         state["rephrased_question"] = better
#     else:
#         state["rephrased_question"] = state["question"].content
#         print(f"[question_rewriter] No history; using original: {state['rephrased_question']}")
#     return state
#
# def question_classifier(state: AgentState) -> AgentState:
#     print("=== Entering question_classifier ===")
#     system_message = SystemMessage(
#         content=(
#             "Classify the user's request into one of three labels:\n"
#             "- 'rice' if it's about rice farming (cultivation, water, fertilizer, AWD, straw, IPM, pests, harvest, etc.).\n"
#             "- 'chitchat' if it's greeting, small talk, identity questions, name/age, 'how are you', thanks, jokes, etc.\n"
#             "- 'offtopic' otherwise."
#         )
#     )
#     human_message = HumanMessage(content=f"User message: {state['rephrased_question']}\nLabel:")
#     grade_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
#     grader_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).with_structured_output(GradeLabel)
#     result = (grade_prompt | grader_llm).invoke({})
#     state["label"] = result.label.strip().lower()
#     print(f"[question_classifier] label = {state['label']}")
#     return state
#
# def route_classifier(state: AgentState) -> str:
#     print("=== Entering route_classifier ===")
#     label = state.get("label", "")
#     if label == "rice":
#         print("[route_classifier] -> retrieve_planner")
#         return "retrieve_planner"
#     elif label == "chitchat":
#         print("[route_classifier] -> chit_chat")
#         return "chit_chat"
#     else:
#         print("[route_classifier] -> off_topic_response")
#         return "off_topic_response"
#
# def retrieve_planner(state: AgentState) -> AgentState:
#     print("=== Entering retrieve_planner ===")
#     question = state["rephrased_question"]
#     messages = [planner_system, HumanMessage(content=f"Plan retrieval for: {question}")]
#     ai = planner_llm.invoke(messages)
#     state.setdefault("messages", [])
#     state["messages"].append(ai)
#     print(f"[retrieve_planner] Tool calls planned: {getattr(ai, 'tool_calls', [])}")
#     return state
#
# tool_node = ToolNode(TOOLS)
#
# def collect_tool_results(state: AgentState) -> AgentState:
#     print("=== Entering collect_tool_results ===")
#     tool_msgs = [m for m in state["messages"] if isinstance(m, ToolMessage)]
#     hits_all: List[Dict[str, Any]] = []
#     for tm in tool_msgs:
#         payload: Dict[str, Any] = {}
#         if isinstance(tm.content, str):
#             import json
#             try:
#                 payload = json.loads(tm.content)
#             except Exception:
#                 payload = {}
#         elif isinstance(tm.content, dict):
#             payload = tm.content
#         hits_all.extend(payload.get("hits", []))
#
#     # Dedupe by chunk_id, keep best score
#     best_by_chunk: Dict[str, Dict[str, Any]] = {}
#     for h in hits_all:
#         cid = h.get("chunk_id") or f"row_{len(best_by_chunk)}"
#         if cid not in best_by_chunk or h.get("score", 0) > best_by_chunk[cid].get("score", 0):
#             best_by_chunk[cid] = h
#     ordered = sorted(best_by_chunk.values(), key=lambda x: x.get("score", 0), reverse=True)
#     docs: List[Document] = []
#     for h in ordered:
#         docs.append(Document(
#             page_content=h.get("content", ""),
#             metadata={
#                 "score": h.get("score", 0.0),
#                 "title": h.get("title", ""),
#                 "summary": h.get("summary", ""),
#                 "url": h.get("url", ""),
#                 "source": h.get("source", ""),
#                 "chunk_id": h.get("chunk_id", ""),
#             }
#         ))
#     state["documents"] = docs
#     print(f"[collect_tool_results] Collected {len(docs)} documents")
#     return state
#
# def retrieval_grader(state: AgentState) -> AgentState:
#     print("=== Entering retrieval_grader ===")
#     relevant_docs: List[Document] = []
#     for doc in state["documents"]:
#         system_message = SystemMessage(content="You are a grader assessing relevance. Reply 'Yes' or 'No'.")
#         human_message = HumanMessage(content=f"User question: {state['rephrased_question']}\n\nRetrieved:\n{doc.page_content}")
#         grade_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
#         grader_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).with_structured_output(GradeDocument)
#         result = (grade_prompt | grader_llm).invoke({})
#         print(f"[retrieval_grader] Doc preview: {doc.page_content[:30]!r} -> {result.score.strip()}")
#         if result.score.strip().lower() == "yes":
#             relevant_docs.append(doc)
#     state["documents"] = relevant_docs
#     state["proceed_to_generate"] = len(relevant_docs) > 0
#     print(f"[retrieval_grader] proceed_to_generate = {state['proceed_to_generate']} (kept {len(relevant_docs)})")
#     return state
#
# def proceed_router(state: AgentState) -> str:
#     print("=== Entering proceed_router ===")
#     if state.get("proceed_to_generate", False):
#         print("[proceed_router] -> generate_answer")
#         return "generate_answer"
#     elif state.get("rephrase_count", 0) >= 2:
#         print("[proceed_router] -> cannot_answer")
#         return "cannot_answer"
#     else:
#         print("[proceed_router] -> refine_question")
#         return "refine_question"
#
# def refine_question(state: AgentState) -> AgentState:
#     print("=== Entering refine_question ===")
#     if state.get("rephrase_count", 0) >= 2:
#         return state
#     q = state["rephrased_question"]
#     system_message = SystemMessage(content="Slightly refine the question to improve retrieval.")
#     human_message = HumanMessage(content=f"Original question: {q}\n\nProvide a slightly refined question.")
#     refine_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
#     resp = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY).invoke(refine_prompt.format())
#     refined = resp.content.strip()
#     print(f"[refine_question] Refined: {refined}")
#     state["rephrased_question"] = refined
#     state["rephrase_count"] = state.get("rephrase_count", 0) + 1
#     return state
#
# def generate_answer(state: AgentState) -> AgentState:
#     print("=== Entering generate_answer ===")
#     history = state["messages"]
#     documents = state["documents"]
#     rq = state["rephrased_question"]
#     context_str = "\n\n".join(doc.page_content for doc in documents)
#     response = rag_chain.invoke({"history": history, "context": context_str, "question": rq})
#     generation = response.content.strip()
#
#     sources_md = format_document_details(documents)
#     final_text = f"{generation}\n\n---\n### Sources used\n{sources_md}"
#
#     state["messages"].append(AIMessage(content=final_text))
#     print("[generate_answer] Done. (Answer + sources appended to state['messages'])")
#     return state
#
# def chit_chat(state: AgentState) -> AgentState:
#     print("=== Entering chit_chat ===")
#     # Keep it friendly and short; no retrieval
#     human = HumanMessage(content=state["question"].content)
#     resp = chitchat_llm.invoke([chitchat_system, human])
#     state.setdefault("messages", [])
#     state["messages"].append(AIMessage(content=resp.content.strip()))
#     return state
#
# def cannot_answer(state: AgentState) -> AgentState:
#     print("=== Entering cannot_answer ===")
#     state.setdefault("messages", [])
#     state["messages"].append(AIMessage(content="I'm sorry, but I couldn't find enough information to answer that clearly."))
#     return state
#
# def off_topic_response(state: AgentState) -> AgentState:
#     print("=== Entering off_topic_response ===")
#     state.setdefault("messages", [])
#     state["messages"].append(
#         AIMessage(content="I'm focused on rice farming topics. Ask me about cultivation, water, fertilizer, IPM, AWD, harvest, markets, etc.")
#     )
#     return state
#
# # =========================
# # Graph
# # =========================
# workflow = StateGraph(AgentState)
#
# # Nodes
# workflow.add_node("question_rewriter", question_rewriter)
# workflow.add_node("question_classifier", question_classifier)
# workflow.add_node("retrieve_planner", retrieve_planner)
# workflow.add_node("tools", tool_node)
# workflow.add_node("collect_tool_results", collect_tool_results)
# workflow.add_node("retrieval_grader", retrieval_grader)
# workflow.add_node("generate_answer", generate_answer)
# workflow.add_node("refine_question", refine_question)
# workflow.add_node("cannot_answer", cannot_answer)
# workflow.add_node("off_topic_response", off_topic_response)
# workflow.add_node("chit_chat", chit_chat)
#
# # Edges
# workflow.add_edge("question_rewriter", "question_classifier")
# workflow.add_conditional_edges(
#     "question_classifier",
#     route_classifier,
#     {
#         "retrieve_planner": "retrieve_planner",
#         "chit_chat": "chit_chat",
#         "off_topic_response": "off_topic_response",
#     },
# )
#
# workflow.add_edge("retrieve_planner", "tools")
# workflow.add_edge("tools", "collect_tool_results")
# workflow.add_edge("collect_tool_results", "retrieval_grader")
#
# workflow.add_conditional_edges(
#     "retrieval_grader",
#     proceed_router,
#     {
#         "generate_answer": "generate_answer",
#         "refine_question": "refine_question",
#         "cannot_answer": "cannot_answer",
#     },
# )
# workflow.add_edge("refine_question", "retrieve_planner")
#
# # End nodes
# workflow.add_edge("generate_answer", END)
# workflow.add_edge("cannot_answer", END)
# workflow.add_edge("off_topic_response", END)
# workflow.add_edge("chit_chat", END)
#
# # Compile with memory checkpointer (per thread)
# workflow.set_entry_point("question_rewriter")
# checkpointer = MemorySaver()
# graph = workflow.compile(checkpointer=checkpointer)
#
# # =========================
# # Streaming helpers
# # =========================
# def stream_answer(question: str, thread_id: Any):
#     """
#     Yields assistant text increments using LangGraph streaming with flush=True.
#     Use this in Streamlit:
#         for chunk in stream_answer(user_text, chat_id): st.write_stream(chunk)
#     """
#     input_data = {"question": HumanMessage(content=question)}
#     last_printed = ""
#
#     for state_update in graph.stream(
#         input=input_data,
#         config={"configurable": {"thread_id": thread_id}},
#         stream_mode="values",
#         # flush=True ensures partial values are emitted ASAP (works with Streamlit)
#         flush=True,
#     ):
#         # We stream only when an AIMessage appears/changes
#         msgs: Optional[List[BaseMessage]] = state_update.get("messages") if isinstance(state_update, dict) else None
#         if not msgs:
#             continue
#         ai_msgs = [m for m in msgs if isinstance(m, AIMessage)]
#         if not ai_msgs:
#             continue
#         content = ai_msgs[-1].content
#         if not isinstance(content, str):
#             continue
#         # yield only the new delta
#         if len(content) > len(last_printed) and content.startswith(last_printed):
#             delta = content[len(last_printed):]
#             last_printed = content
#             if delta:
#                 yield delta
#         else:
#             # fallback (first token or re-sync)
#             last_printed = content
#             yield content
#
# # =========================
# # CLI loop (supports /new and /stream)
# # =========================
# if __name__ == "__main__":
#     print("RiceAI Agent — type '/new' for a fresh thread, '/stream' to toggle streaming, 'quit' to exit.")
#     thread_id = "default-thread"
#     streaming = False
#
#     while True:
#         user_q = input("You: ").strip()
#         if user_q.lower() in {"quit", "exit"}:
#             break
#         if user_q.lower() == "/new":
#             import uuid
#             thread_id = str(uuid.uuid4())[:8]
#             print(f"[system] New thread_id = {thread_id}")
#             continue
#         if user_q.lower() == "/stream":
#             streaming = not streaming
#             print(f"[system] Streaming is now {'ON' if streaming else 'OFF'}")
#             continue
#
#         input_data = {"question": HumanMessage(content=user_q)}
#
#         if streaming:
#             print("Assistant: ", end="", flush=True)
#             for piece in stream_answer(user_q, thread_id):
#                 print(piece, end="", flush=True)
#             print("\n" + "-" * 40)
#         else:
#             result = graph.invoke(input=input_data, config={"configurable": {"thread_id": thread_id}})
#             if "messages" in result and result["messages"]:
#                 replies = [m for m in result["messages"] if isinstance(m, AIMessage)]
#                 if replies:
#                     print("\nAssistant:\n" + replies[-1].content)
#                 else:
#                     print("\nAssistant: (no AI reply)")
#             else:
#                 print("\nAssistant: (no response)")
#             print("-" * 40)