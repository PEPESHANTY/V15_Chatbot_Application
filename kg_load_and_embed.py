"""
kg_load_and_embed.py
--------------------
Loads all chapter Cypher files from a folder (default: cypher_queries_NEW/)
and then embeds ALL :Searchable nodes missing `embedding` exactly once.

- Expects per-chapter files to define a top-level variable:  cypher = """  """
- Works whether the folder is a Python package or just a plain folder
  (we use runpy.run_path to read 'cypher' from each .py file).
- Requires env: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, OPENAI_API_KEY
  Optional: OPENAI_BASE_URL, EMBED_MODEL (default text-embedding-3-small)

Usage examples:
    python kg_load_and_embed.py                              # load & embed
    python kg_load_and_embed.py --skip-embed                 # only load
    python kg_load_and_embed.py --skip-load                  # only embed (resume)
    python kg_load_and_embed.py --folder cypher_queries_NEW  # different folder
    python kg_load_and_embed.py --batch 256                  # embedding batch size
"""

import os
import sys
import time
import argparse
import runpy
from typing import List, Dict, Any

from dotenv import load_dotenv
from openai import OpenAI
from langchain_neo4j import Neo4jGraph

# ─────────────────────────────────────────────────────────────
# Env & Clients
# ─────────────────────────────────────────────────────────────
load_dotenv()

NEO4J_URI      = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")  # e.g., http://hanoi2.ucd.ie/v1
OPENAI_API_KEY  = os.environ["OPENAI_API_KEY"]
EMBED_MODEL     = os.getenv("EMBED_MODEL", "text-embedding-3-small")

kg = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

VEC_INDEX = "searchable_embedding_idx"

# ─────────────────────────────────────────────────────────────
# Vector index setup
# ─────────────────────────────────────────────────────────────
def probe_dim() -> int:
    v = client.embeddings.create(model=EMBED_MODEL, input="dimension probe").data[0].embedding
    return len(v)

def ensure_vector_index(dim: int):
    kg.query(f"""
    CREATE VECTOR INDEX {VEC_INDEX} IF NOT EXISTS
    FOR (n:Searchable) ON (n.embedding)
    OPTIONS {{
      indexConfig: {{ `vector.dimensions`: {dim}, `vector.similarity_function`: 'cosine' }}
    }}
    """)

# ─────────────────────────────────────────────────────────────
# Loader: run every cypher file in the folder
# ─────────────────────────────────────────────────────────────
def discover_cypher_files(folder: str) -> List[str]:
    files = []
    for name in sorted(os.listdir(folder)):
        if name.endswith(".py") and not name.startswith("__"):
            files.append(os.path.join(folder, name))
    return files

def extract_cypher_from_py(path: str) -> str:
    ns = runpy.run_path(path)
    if "cypher" not in ns or not isinstance(ns["cypher"], str):
        raise ValueError(f"{os.path.basename(path)} must define a string variable named 'cypher'")
    return ns["cypher"]

def run_all_cypher(folder: str) -> None:
    files = discover_cypher_files(folder)
    if not files:
        print(f"⚠️  No .py Cypher files found in {folder}")
        return
    for i, path in enumerate(files, start=1):
        name = os.path.basename(path)
        try:
            print(f"🚀 [{i}/{len(files)}] Running {name} ...")
            cypher = extract_cypher_from_py(path)
            kg.query(cypher)
            print(f"✅ Finished {name}\n")
        except Exception as e:
            print(f"❌ Error in {name}: {e}\n")

# ─────────────────────────────────────────────────────────────
# Embedding: once for the whole graph (all chapters)
# ─────────────────────────────────────────────────────────────
def fetch_nodes_to_embed(limit: int) -> List[Dict[str, Any]]:
    return kg.query("""
        MATCH (n:Searchable)
        WHERE n.search_text IS NOT NULL
          AND (n.embedding IS NULL OR size(n.embedding) = 0)
        RETURN n.entity_id AS id, n.search_text AS text
        LIMIT $lim
    """, {"lim": limit})

def write_embeddings(rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    kg.query("""
        UNWIND $rows AS r
        MATCH (n:Searchable {entity_id: r.id})
        SET n.embedding = r.embedding
    """, {"rows": rows})

def embed_missing_all(batch: int = 256, sleep_s: float = 0.0) -> int:
    total = 0
    dim = probe_dim()
    ensure_vector_index(dim)
    print(f"🔧 Vector index ensured (dim={dim}).")

    while True:
        rows = fetch_nodes_to_embed(batch)
        if not rows:
            break
        texts = [r["text"] for r in rows]
        embs  = client.embeddings.create(model=EMBED_MODEL, input=texts).data
        out   = [{"id": r["id"], "embedding": e.embedding} for r, e in zip(rows, embs)]
        write_embeddings(out)
        total += len(out)
        print(f"🧠 Embedded {len(out)} nodes (cumulative {total})")
        if sleep_s > 0:
            time.sleep(sleep_s)

    print(f"✅ Embedding complete. Total nodes embedded: {total}")
    return total

# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Load Cypher queries and embed once across all chapters.")
    ap.add_argument("--folder", default="cypher_queries_NEW", help="Folder containing *.py Cypher files")
    ap.add_argument("--batch", type=int, default=256, help="Embedding batch size")
    ap.add_argument("--sleep", type=float, default=0.0, help="Sleep seconds between embed batches (rate-limit cushion)")
    ap.add_argument("--skip-load", action="store_true", help="Skip running Cypher files; only embed missing")
    ap.add_argument("--skip-embed", action="store_true", help="Skip embedding; only run Cypher files")
    args = ap.parse_args()

    if not os.path.isdir(args.folder):
        print(f"❌ Folder not found: {args.folder}")
        sys.exit(1)

    if not args.skip_load:
        run_all_cypher(args.folder)

    if not args.skip_embed:
        embed_missing_all(batch=args.batch, sleep_s=args.sleep)

if __name__ == "__main__":
    main()
