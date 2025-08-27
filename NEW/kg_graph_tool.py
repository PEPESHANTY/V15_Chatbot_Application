"""
kg_graph_tool.py
----------------
KG-RAG query tool built from your notebook Cells 1–9 (original retrieval logic)
with:
- auto chapter detection (no need to pass chapter=)
- formatted numbered list with **bold** headings + inline [entity_id] citations
- appended "Top hits:" block with scores

Embeddings must already exist (populate via your loader).
"""

import os
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI
from langchain_neo4j import Neo4jGraph

# ─────────────────────────────────────────────────────────────
# Setup (matches your notebook Cell 1)
# ─────────────────────────────────────────────────────────────
load_dotenv()

NEO4J_URI      = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")     # e.g., http://hanoi2.ucd.ie/v1 (or None for OpenAI)
OPENAI_API_KEY  = os.environ["OPENAI_API_KEY"]
EMBED_MODEL     = os.getenv("EMBED_MODEL", "text-embedding-3-small")
CHAT_MODEL      = os.getenv("CHAT_MODEL", "gpt-4o-mini")

VEC_INDEX = "searchable_embedding_idx"

_kg = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
_client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

# ─────────────────────────────────────────────────────────────
# Helpers: chapter inference / selection
# ─────────────────────────────────────────────────────────────
_CHAPTER_REGEX = re.compile(r"\bch(?:apter)?\s*([0-9]{1,2})\b", flags=re.IGNORECASE)

def _infer_chapter_from_question(q: str) -> Optional[str]:
    """'chapter 1', 'ch1', 'ch 1' -> 'Ch1'. None if no match."""
    m = _CHAPTER_REGEX.search(q or "")
    return f"Ch{int(m.group(1))}" if m else None

def _best_hit_chapter(hits: List[Dict[str, Any]]) -> Optional[str]:
    """Pick the chapter of the best (closest) hit if present."""
    if not hits:
        return None
    return hits[0].get("chapter")

# ─────────────────────────────────────────────────────────────
# Cell 5 — embed_text + vector_search_nodes (original behavior)
# ─────────────────────────────────────────────────────────────
def embed_text(text: str) -> List[float]:
    return _client.embeddings.create(model=EMBED_MODEL, input=text).data[0].embedding

def vector_search_nodes(question: str, top_k: int = 8, chapter: Optional[str] = None) -> List[Dict[str, Any]]:
    qvec = embed_text(question)
    params: Dict[str, Any] = {"k": top_k, "qvec": qvec}
    chapter_filter = "AND node.chapter = $chapter" if chapter else ""
    if chapter:
        params["chapter"] = chapter
    cypher = f"""
    WITH $qvec AS qv
    CALL db.index.vector.queryNodes('{VEC_INDEX}', $k, qv)
    YIELD node, score
    WHERE node.search_text IS NOT NULL {chapter_filter}
    RETURN labels(node) AS labels,
           node.entity_id AS id,
           coalesce(node.name, node.entity_id) AS name,
           node.summary AS summary,
           node.description AS description,
           node.chapter AS chapter,
           score
    ORDER BY score ASC
    """
    return _kg.query(cypher, params)

# ─────────────────────────────────────────────────────────────
# Cell 6 — robust 1-hop subgraph expansion
# ─────────────────────────────────────────────────────────────
def expand_entities(ids: List[str], per_node_limit: int = 25) -> List[Dict[str, Any]]:
    if not ids:
        return []
    return _kg.query("""
        MATCH (n:Searchable) WHERE n.entity_id IN $ids
        MATCH (n)-[r]-(m)
        RETURN
           coalesce(n.entity_id, elementId(n))           AS src_id,
           coalesce(n.name, n.entity_id, labels(n)[0])   AS src_name,
           type(r)                                       AS rel_type,
           coalesce(r.description, r.search_text, '')    AS rel_desc,
           coalesce(m.entity_id, elementId(m))           AS dst_id,
           coalesce(m.name, m.entity_id, labels(m)[0])   AS dst_name,
           m.summary                                     AS dst_summary,
           m.description                                 AS dst_description
        LIMIT $lim
    """, {"ids": ids, "lim": per_node_limit * max(1, len(ids))})

# ─────────────────────────────────────────────────────────────
# Cell 7 — facts + context
# ─────────────────────────────────────────────────────────────
def to_fact(row: Dict[str, Any]) -> Dict[str, Any]:
    rel   = row.get("rel_type") or "RELATED_TO"
    rdesc = (row.get("rel_desc") or "").strip()
    src   = row.get("src_name") or row.get("src_id")
    dst   = row.get("dst_name") or row.get("dst_id")

    fact = f"{src} --{rel}--> {dst}"
    if rdesc:
        fact += f" :: {rdesc}"

    cites = [row.get("src_id"), row.get("dst_id")]
    cites = [c for c in cites if c]
    seen = set()
    cites = [c for c in cites if not (c in seen or seen.add(c))]

    return {"text": fact, "cites": cites}

def build_context(hits: List[Dict[str, Any]], expansions: List[Dict[str, Any]],
                  max_nodes: int = 6, max_facts: int = 20) -> Dict[str, Any]:
    node_cards = []
    for h in hits[:max_nodes]:
        blurb = h.get("summary") or h.get("description") or ""
        if not blurb:
            continue
        node_cards.append({"id": h["id"], "name": h["name"], "blurb": blurb.strip()})

    clean_rows = [r for r in expansions if (r.get("src_id") or r.get("dst_id"))]
    facts = [to_fact(r) for r in clean_rows][:max_facts]
    return {"nodes": node_cards, "facts": facts}

# ─────────────────────────────────────────────────────────────
# "Top hits" rendering
# ─────────────────────────────────────────────────────────────
def _render_top_hits(hits: List[Dict[str, Any]], n: int = 5) -> str:
    lines = []
    for x in hits[:n]:
        _id = x.get("id", "")
        _name = x.get("name", _id)
        try:
            sc = float(x.get("score", 0.0))
            score_str = f"{sc:.4f}"
        except Exception:
            score_str = str(x.get("score"))
        lines.append(f"- [{_id}] {_name} (score={score_str})")
    return "Top hits:\n" + "\n".join(lines)

# ─────────────────────────────────────────────────────────────
# Cell 8 — LLM answerer (with format hint)
# ─────────────────────────────────────────────────────────────
def answer_with_llm(question: str, context: Dict[str, Any], format_hint: Optional[str] = None) -> str:
    fact_lines = [f"- {f['text']} [refs: {', '.join(f['cites'])}]" for f in context["facts"]]
    node_lines = [f"- ({n['id']}) {n['name']}: {n['blurb']}" for n in context["nodes"]]

    system = (
        "You are RiceAI Expert. Answer using ONLY the provided facts and notes.\n"
        "Cite using the provided entity_ids in square brackets like [Ch1] or [Straw Management].\n"
        "Be precise and concise."
    )
    style = (
        "\n\nOUTPUT FORMAT (strict):\n"
        "Return a detailed, numbered list when appropriate. Each item must be:\n"
        "1. **Short Title** in bold (e.g., **Straw Management**)\n"
        "2. Colon\n"
        "3. One–two sentence description, grounded in the facts\n"
        "4. Inline citations like [Straw Management, Ch1] (use provided entity_ids)\n"
        "No extra sections besides the list (we will append Top hits ourselves)."
    )
    if format_hint:
        style += "\n\nAdditional formatting guidance:\n" + format_hint

    user = (
        f"Question: {question}\n\n"
        f"Nodes:\n" + "\n".join(node_lines[:10]) + "\n\n"
        f"Facts:\n" + "\n".join(fact_lines[:25]) +
        style
    )
    resp = _client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.1
    )
    return resp.choices[0].message.content.strip()

# ─────────────────────────────────────────────────────────────
# ask(): now **auto-detects chapter** if not provided
# ─────────────────────────────────────────────────────────────
def ask(question: str,
        chapter: Optional[str] = None,
        top_k: int = 8,
        expand: int = 4,
        per_node_limit: int = 25,
        detailed: bool = True) -> Dict[str, Any]:
    """
    1) If chapter=None:
         - try to infer chapter from the question text (e.g., "chapter 1" -> "Ch1")
         - run vector search (restricted if inferred)
         - if still None or empty, run broad search; take top hit's chapter and re-run restricted
       Else: run vector search restricted to the provided chapter
    2) 1-hop expand on the final hit set
    3) LLM answer with citations (numbered list with bold headings)
    4) Append a 'Top hits:' block with scores
    """
    inferred = chapter or _infer_chapter_from_question(question)

    # First pass: if we have a chapter (explicit or inferred), try with it
    hits = vector_search_nodes(question, top_k=top_k, chapter=inferred) if inferred else []
    # Fallback: broad search
    if not hits:
        hits = vector_search_nodes(question, top_k=top_k, chapter=None)

    # If we didn’t start with a chapter, pick the best-hit chapter and refine
    final_chapter = inferred or _best_hit_chapter(hits)
    if final_chapter:
        refined = vector_search_nodes(question, top_k=top_k, chapter=final_chapter)
        if refined:
            hits = refined

    ids  = [x["id"] for x in hits[:expand]]
    ex   = expand_entities(ids, per_node_limit=per_node_limit)
    context = build_context(hits, ex)

    format_hint = "Make it a numbered list with bold headings and inline citations for each item."
    answer_body = answer_with_llm(question, context, format_hint=format_hint if detailed else None)
    top_block   = _render_top_hits(hits, n=5)
    final       = f"{answer_body}\n\n{top_block}"

    return {"answer": final, "hits": hits, "facts": context["facts"]}

# ─────────────────────────────────────────────────────────────
# Optional CLI
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="KG graph tool (vector search + 1-hop). Embeddings must already exist.")
    p.add_argument("-q", "--question", required=True)
    p.add_argument("-c", "--chapter", default=None)
    p.add_argument("--top_k", type=int, default=8)
    p.add_argument("--expand", type=int, default=4)
    p.add_argument("--per_node_limit", type=int, default=25)
    args = p.parse_args()

    res = ask(args.question, chapter=args.chapter, top_k=args.top_k, expand=args.expand, per_node_limit=args.per_node_limit)
    print("\n=== ANSWER ===")
    print(res["answer"])
