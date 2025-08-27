from dotenv import load_dotenv
import os
import importlib
import re
from langchain_neo4j import Neo4jGraph
from openai import OpenAI

# ── ENV ───────────────────────────────────────────────────────────────
load_dotenv()
NEO4J_URI      = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")   # e.g. http://hanoi2.ucd.ie/v1  (or leave None for OpenAI)
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
EMBED_MODEL     = os.getenv("EMBED_MODEL", "text-embedding-3-small")

# ── CLIENTS ───────────────────────────────────────────────────────────
kg = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

# ── CONFIG ────────────────────────────────────────────────────────────
CYPHER_QUERY_FOLDER = "cypher_queries_NEW"
BATCH = 256

# ── UTILITIES ─────────────────────────────────────────────────────────
def probe_dim() -> int:
    """Probe the embedding dimension from the model."""
    v = client.embeddings.create(model=EMBED_MODEL, input="dimension probe").data[0].embedding
    return len(v)

def ensure_vector_index(dim: int):
    """Create a Neo4j vector index over :Searchable(embedding) if missing."""
    kg.query(f"""
    CREATE VECTOR INDEX searchable_embedding_idx IF NOT EXISTS
    FOR (n:Searchable) ON (n.embedding)
    OPTIONS {{
      indexConfig: {{ `vector.dimensions`: {dim}, `vector.similarity_function`: 'cosine' }}
    }}
    """)

def fetch_to_embed_for_chapter(chapter_tag: str, limit: int = BATCH):
    """Fetch Searchable nodes for a specific chapter lacking embeddings."""
    return kg.query("""
        MATCH (n:Searchable)
        WHERE n.chapter = $chapter
          AND n.search_text IS NOT NULL
          AND (n.embedding IS NULL OR size(n.embedding) = 0)
        RETURN n.entity_id AS id, n.search_text AS text
        LIMIT $lim
    """, {"chapter": chapter_tag, "lim": limit})

def set_embeddings(rows):
    """Write back embeddings."""
    if not rows:
        return
    kg.query("""
        UNWIND $rows AS r
        MATCH (n:Searchable {entity_id: r.id})
        SET n.embedding = r.embedding
    """, {"rows": rows})

def embed_chapter(chapter_tag: str, batch: int = BATCH):
    """Batch-embed a chapter's Searchable nodes."""
    print(f"🔎 Embedding nodes for {chapter_tag} ...")
    while True:
        rows = fetch_to_embed_for_chapter(chapter_tag, batch)
        if not rows:
            break
        texts = [r["text"] for r in rows]
        embs  = client.embeddings.create(model=EMBED_MODEL, input=texts).data
        out   = [{"id": r["id"], "embedding": e.embedding} for r, e in zip(rows, embs)]
        set_embeddings(out)

def chapter_tag_from_filename(filename: str) -> str:
    """Map 'chapter_1.py' -> 'Ch1', 'chapter_02.py' -> 'Ch2'."""
    digits = re.findall(r"\d+", filename)
    n = int(digits[0]) if digits else 1
    return f"Ch{n}"

def run_all_chapters():
    # Ensure vector index up front (once)
    dim = probe_dim()
    ensure_vector_index(dim)

    for filename in sorted(os.listdir(CYPHER_QUERY_FOLDER)):
        if not (filename.endswith(".py") and not filename.startswith("__")):
            continue

        module_name = filename[:-3]  # strip .py
        module_path = f"{CYPHER_QUERY_FOLDER}.{module_name}"

        try:
            print(f"🚀 Running {filename} ...")
            mod = importlib.import_module(module_path)
            # Insert/Upsert graph content
            kg.query(mod.cypher)

            # Embed immediately after inserting
            tag = chapter_tag_from_filename(filename)
            embed_chapter(tag)

            print(f"✅ Finished {filename}\n")
        except Exception as e:
            print(f"❌ Error in {filename}: {e}\n")

if __name__ == "__main__":
    run_all_chapters()
