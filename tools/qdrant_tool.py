from langchain_core.tools import Tool
from langchain_core.documents import Document
from typing import List
from tools.crosslingual_retriever import retrieve_chunks_crosslingual


def run_qdrant_search(query: str) -> str:
    """
    Retrieves relevant chunks from Qdrant based on the query (cross-lingual).
    Returns a formatted string answer for the agent.
    """
    chunks = retrieve_chunks_crosslingual(query, top_k=5)

    if not chunks:
        return "No relevant content found in the rice document collection."

    response_lines = ["Here are the most relevant rice-related sources:\n"]

    for i, chunk in enumerate(chunks, 1):
        response_lines.append(
            f"{i}. **Title**: {chunk.get('title', 'N/A')}  (Score: {chunk.get('score'):.3f})\n"
            f"   ├─ Chunk ID: {chunk.get('chunk_id', 'N/A')}\n"
            f"   ├─ URL: {chunk.get('url', 'N/A')}\n"
            f"   ├─ Summary: {chunk.get('summary', '')[:150]}...\n"
            f"   └─ Content Preview: {chunk.get('content', '')[:200]}...\n"
        )

    return "\n".join(response_lines)


# ✅ LangChain-compatible tool
QdrantRetrieverTool = Tool.from_function(
    func=run_qdrant_search,
    name="qdrant_rice_search",
    description="Use this tool to search for rice-related information (fertilizer, variety, pests, water, yield, climate, IPM, etc.) from the RiceAI document collection using vector similarity.",
    return_direct=True,
)
