from typing import Any

from packages.pocket_agent.eth_tools import POKT_eth_getBalance
from langchain.agents import AgentExecutor

from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI


class AgentInput(BaseModel):
    input: str


class AgentOutput(BaseModel):
    output: Any


def get_agent():
    ETH_balance_tool = POKT_eth_getBalance()
    tools = [ETH_balance_tool]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    llm_with_tools = llm.bind_tools(tools)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True).with_types(input_type=AgentInput, output_type=AgentOutput)

    return agent_executor

agent = get_agent()
