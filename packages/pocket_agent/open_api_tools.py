import os
from typing import Optional, Type, Union

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.chains import OpenAPIEndpointChain
from langchain.requests import Requests
from langchain.tools import APIOperation, BaseTool, OpenAPISpec
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.pydantic_v1 import BaseModel, Field

POCKET_NEWTWORK_ETH_OPEN_API_DOCS = os.getenv("POCKET_NEWTWORK_ETH_OPEN_API_DOCS")


def create_open_api_chain(llm):

    # Get spec from github
    spec = OpenAPISpec.from_url(POCKET_NEWTWORK_ETH_OPEN_API_DOCS)

    # Select the path and method to use in the chain
    operation = APIOperation.from_openapi_spec(spec, "/", "post")

    # Create chain
    chain = OpenAPIEndpointChain.from_api_operation(
        operation,
        llm,
        requests=Requests(),
        verbose=True,
        return_intermediate_steps=True,  # Return request and response text
    )

    return chain


################################################################################
# ------------------------------ Create Tool --------------------------------- #
################################################################################

# Tool input schema
class POKT_eth_getBalanceSchema_openAPI(BaseModel):
    address: str = Field(
        description="The Ethereum address to check for balance",
    )
    blockNumber: str = Field(
        default="latest",
        description='The block number or the string latest, earliest, pending, safe or finalized. If not provided, use "latest".',
    )


# Tool definition
class POKT_eth_getBalance_openAPI(BaseTool):
    """
    This tool is just a wrap of the openAPI chain.
    """

    name: str = "eth_getBalance"
    description: str = "Returns the balance of the account of a given address."
    args_schema: Type[POKT_eth_getBalanceSchema_openAPI] = POKT_eth_getBalanceSchema_openAPI
    openAPI_chain: OpenAPIEndpointChain

    def _run(
        self,
        address: str,
        blockNumber: str = "latest",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        # Simply call the openAPI chain...
        return self.openAPI_chain.invoke({"instructions": f"Get balance of account {address} at height {blockNumber}"})

    async def _arun(
        self,
        address: str,
        blockNumber: str = "latest",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        # Simply call the openAPI chain...
        return await self.openAPI_chain.ainvoke(
            {"instructions": f"Get balance of account {address} at height {blockNumber}"}
        )


# Helper function to crete tool
def get_eth_balance_tool(
    llm: Union[BaseChatModel, BaseLanguageModel],
):

    tool = POKT_eth_getBalance_openAPI(
        openAPI_chain=create_open_api_chain(llm),
    )
    return tool
