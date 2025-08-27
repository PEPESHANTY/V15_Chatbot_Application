from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.types import Command

from langchain_core.tools import Tool
from tools.qdrant_tool import QdrantRetrieverTool

from langchain.agents import RunnableAgent
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.prompts import AgentPrompt


# ✅ Define the LangGraph state type
class MessagesState(TypedDict):
    messages: List[BaseMessage]


# ✅ Build your agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [QdrantRetrieverTool]
prompt = AgentPrompt.from_tools(tools)

agent = RunnableAgent(
    llm=llm.bind_tools(tools),
    prompt=prompt,
    output_parser=OpenAIToolsAgentOutputParser()
)


# ✅ Exported function required by LangGraph
def vector_agent_node(state: MessagesState) -> Command[str]:
    result = agent.invoke(state)

    return Command(
        update={"messages": state["messages"] + [result]},
        goto="end"
    )
