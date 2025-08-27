import os
from pathlib import Path
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# -- Load environment variables --
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

def get_query_embedding(text: str) -> List[float]:
    """Return the OpenAI embedding for a text query."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def retrieve_chunks(query: str, k: int = 5, threshold: float = 0.35) -> List[Dict]:
    """
    Retrieve top-k relevant chunks from Qdrant and return them as dictionaries.
    Each dictionary contains score, content, and metadata fields.
    """
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    query_vector = get_query_embedding(query)

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=k,
        with_payload=True,
        with_vectors=False,
        score_threshold=threshold
    )

    chunks: List[Dict] = []
    for r in results:
        payload = r.payload or {}
        chunks.append({
            "score": r.score,
            "content": payload.get("content", ""),
            "title": payload.get("title", ""),
            "summary": payload.get("summary", ""),
            "url": payload.get("url", ""),
            "source": payload.get("source", ""),
            "chunk_id": payload.get("chunk_id", "")
        })

    # Apply local threshold filter
    return [c for c in chunks if c["score"] >= threshold]

def retrieve_context_text(query: str, k: int = 5, threshold: float = 0.35) -> str:
    """Concatenate the content of the retrieved chunks into one context string."""
    chunks = retrieve_chunks(query, k=k, threshold=threshold)
    return "\n\n".join(chunk["content"] for chunk in chunks)

def answer_query(
    query: str, k: int = 5, threshold: float = 0.35, return_docs: bool = False
) -> Tuple[str, List[Document] | None]:
    """
    Use Qdrant retrieval to build context and ask the LLM to answer the query.
    If return_docs=True, also return the retrieved chunk documents with metadata.
    """
    chunks = retrieve_chunks(query, k=k, threshold=threshold)
    context = "\n\n".join(c["content"] for c in chunks)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are RiceAI Expert, a trusted agronomist and AI agent trained on "
            "sustainable and high-yield rice farming practices. Answer the question "
            "based on the following context:\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{question}\n\n"
            "Answer:"
        )
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)
    formatted_prompt = prompt.format(context=context, question=query)
    response = llm.invoke(formatted_prompt)
    answer_text = response.content

    # If caller wants documents, wrap chunks in LangChain Document objects
    docs: List[Document] | None = None
    if return_docs:
        docs = [
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
            for c in chunks
        ]

    return answer_text, docs

# Example usage
if __name__ == "__main__":
    user_question = "What are the key factors affecting organic fertilizer adoption in rice production?"
    answer, docs = answer_query(user_question, k=5, threshold=0.35, return_docs=True)
    print(answer)

    # Print the retrieved documents for debugging / inspection
    if docs:
        print("\nRetrieved documents:")
        for i, doc in enumerate(docs, 1):
            meta = doc.metadata
            print(f"{i}. Title: {meta.get('title', 'N/A')} (score: {meta.get('score', 0):.3f})")
            print(f"   URL: {meta.get('url', 'N/A')}")
            print(f"   Summary: {meta.get('summary', '')[:150]}...")
            print()
