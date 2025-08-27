from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class MessagesState(TypedDict):
    messages: List[BaseMessage]

class SupervisorDecision(BaseModel):
    next: Literal["vector_agent"] = Field(
        description="Only available agent is 'vector_agent' for now."
    )
    reason: str = Field(
        description="Why the vector agent is suitable for answering this query."
    )

llm = ChatOpenAI(model="gpt-4o")

def supervisor_node(state: MessagesState) -> Command[Literal["vector_agent"]]:
    system_prompt = '''
You are a routing supervisor in a rice farming AI system.

Currently, only the vector-based agent (Qdrant) is available. For every question, route to `vector_agent`.
Still, explain *why* vector search is suitable — e.g., the query is unstructured, open-ended, or needs explanation.
    '''

    messages = [{"role": "system", "content": system_prompt}] + state["messages"]

    response = llm.with_structured_output(SupervisorDecision).invoke(messages)

    print(f"--- Supervisor routed to → {response.next.upper()} ---")

    return Command(
        update={
            "messages": [HumanMessage(content=response.reason, name="supervisor")]
        },
        goto=response.next
    )
