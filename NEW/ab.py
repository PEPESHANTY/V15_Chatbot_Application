import os
from pathlib import Path
from typing import List, Dict, Tuple

from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
env_path = Path('.') / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION_NAME")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize clients
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_query_embedding(text: str) -> List[float]:
    """Compute a dense embedding for the query using OpenAI's embedding model."""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def retrieve_chunks(
    query: str, k: int = 5
) -> List[Dict]:
    """
    Retrieve top-k chunks using query_points() without discarding hits
    with unknown score types.
    """
    query_vector = get_query_embedding(query)

    # Do not set score_threshold in query_points so it returns the top-k hits as-is
    response = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=k,
        with_payload=True,
        with_vectors=False,
        score_threshold=None,
    )

    hits = response.result if hasattr(response, "result") else response
    chunks: List[Dict] = []

    for hit in hits:
        # Pull payload and score from either ScoredPoint or tuple
        if hasattr(hit, "payload"):
            raw_payload = hit.payload or {}
            raw_score = hit.score
        elif isinstance(hit, tuple):
            if len(hit) == 3:
                _, raw_payload, raw_score = hit
            else:
                raw_payload, raw_score = hit
        else:
            raw_payload = hit
            raw_score = None

        # Extract text and metadata
        if isinstance(raw_payload, dict):
            content = raw_payload.get("content", "")
            title = raw_payload.get("title", "")
            summary = raw_payload.get("summary", "")
            url = raw_payload.get("url", "")
            source = raw_payload.get("source", "")
            chunk_id = raw_payload.get("chunk_id", "")
        else:
            content = str(raw_payload)
            title = summary = url = source = chunk_id = ""

        # Try to interpret score; if not numeric, skip filtering
        try:
            numeric_score = float(raw_score) if raw_score is not None else 0.0
        except Exception:
            # If score isn't convertible, assign a default
            numeric_score = 0.0

        chunks.append({
            "score": numeric_score,
            "content": content,
            "title": title,
            "summary": summary,
            "url": url,
            "source": source,
            "chunk_id": chunk_id,
        })

    return chunks

def answer_query(
    question: str, k: int = 5, return_docs: bool = False
) -> Tuple[str, List[Document] | List[Dict]]:
    """
    Retrieve context from Qdrant and generate an answer.  Optionally return Document objects.
    """
    chunks = retrieve_chunks(question, k=k)
    context = "\n\n".join(c["content"] for c in chunks)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are RiceAI Expert, a trusted agronomist and AI agent trained on sustainable "
            "and high-yield rice farming practices.\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{question}\n\n"
            "Provide a thorough answer using all relevant information."
        )
    )

    chat = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)
    answer_text = chat.invoke(prompt.format(context=context, question=question)).content

    if return_docs:
        docs: List[Document] = []
        for c in chunks:
            docs.append(
                Document(
                    page_content=c["content"],
                    metadata={
                        "score": c["score"],
                        "title": c["title"],
                        "summary": c["summary"],
                        "url": c["url"],
                        "source": c["source"],
                        "chunk_id": c["chunk_id"],
                    }
                )
            )
        return answer_text, docs

    return answer_text, chunks

if __name__ == "__main__":
    user_question = input("Enter your question: ")
    answer, docs = answer_query(user_question, k=5, return_docs=True)
    print("\nAnswer:\n", answer)

    if docs:
        print("\nRetrieved Chunks (with metadata):")
        for i, doc in enumerate(docs, 1):
            meta = doc.metadata
            print(f"{i}. Title: {meta.get('title', 'N/A')} (score: {meta.get('score', 0):.3f})")
            print(f"   URL: {meta.get('url', 'N/A')}")
            print(f"   Summary: {meta.get('summary', '')[:150]}...")
            print(f"   Preview: {doc.page_content[:200]}...\n")
