from langgraph.graph import StateGraph, END
from agents.vector_agent_node import vector_agent_node
from agents.supervisor_node import supervisor_node
from typing import TypedDict, List
from langchain_core.messages import BaseMessage


class MessagesState(TypedDict):
    messages: List[BaseMessage]


def build_qdrant_only_graph():
    graph = StateGraph(MessagesState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("vector_agent", vector_agent_node)

    graph.set_entry_point("supervisor")
    graph.add_edge("supervisor", "vector_agent")
    graph.add_edge("vector_agent", END)

    return graph.compile()
