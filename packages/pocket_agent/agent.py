import os
from typing import Any

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI

from packages.pocket_agent.eth_tools import POKT_eth_getBalance
from packages.pocket_agent.open_api_tools import get_eth_balance_tool

OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")


class AgentInput(BaseModel):
    input: str


class AgentOutput(BaseModel):
    output: Any


def get_agent(USE_OPEN_API=False):
    # Declare template for chat bot
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that loves the Pocket Network."),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Declare the llm model to use for the chat bot
    llm = ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=0.25)

    # Select tools to use
    if USE_OPEN_API:
        ETH_balance_tool = get_eth_balance_tool(llm)
    else:
        ETH_balance_tool = POKT_eth_getBalance()
    # Create tool list
    tools = [ETH_balance_tool]

    # Bind the tools to the model (only work with llms that have a compatible backend for tools, like openAI or vLLM)
    llm_with_tools = llm.bind_tools(tools)

    # Create the agent
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    # Return the agent executor to langserve
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True).with_types(
        input_type=AgentInput, output_type=AgentOutput
    )

    return agent_executor
