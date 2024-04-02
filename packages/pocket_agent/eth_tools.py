import os
from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional, Tuple, Type, Union

from web3 import Web3, AsyncWeb3, HTTPProvider, AsyncHTTPProvider

POCKET_NEWTWORK_ETH_URL = os.getenv("POCKET_NEWTWORK_ETH_URL")

w3 = Web3(Web3.HTTPProvider(POCKET_NEWTWORK_ETH_URL, request_kwargs={'timeout': 60}))
aw3 = AsyncWeb3(AsyncHTTPProvider(POCKET_NEWTWORK_ETH_URL, request_kwargs={'timeout': 60}))

class POKT_eth_getBalanceSchema(BaseModel):
    address: str = Field(
        description="The Ethereum address to check for balance",        
    )
    blockNumber: str = Field(
        default="latest",
        description="The block number or the string latest, earliest, pending, safe or finalized. If not provided, use \"latest\".",
    )

class POKT_eth_getBalance(BaseTool):
    name: str = "eth_getBalance"
    description: str = "Returns the balance of the account of a given address."
    args_schema: Type[POKT_eth_getBalanceSchema] = POKT_eth_getBalanceSchema


    def _run(
        self,
        address: str,
        blockNumber: str = "latest",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:

        if blockNumber not in ["latest", "earliest", "pending", "safe", "finalized"] and blockNumber.isdigit():
            try:
                blockNumber = w3.to_hex(int(blockNumber))
            except:
                response = "block number provided not valid. Please provide a valid block number and try again."

        if Web3.is_address(address):
            try:
                response = w3.eth.get_balance(address, blockNumber)
            except:
                response = "Sorry, I could't find your balance. Please verify the address and try again."
        else:
            response = "Adress {} is not a valid Ethereum address.".format(address)
        return response

    async def _arun(
        self,
        address: str,
        blockNumber: str = "latest",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:

        if blockNumber not in ["latest", "earliest", "pending", "safe", "finalized"] and blockNumber.isdigit():
            try:
                blockNumber = w3.to_hex(int(blockNumber))
            except:
                response = "block number provided not valid. Please provide a valid block number and try again."

        if Web3.is_address(address):
            try:
                 response = await aw3.eth.get_balance(address, blockNumber)
            except Exception as e:
                response = "Sorry, I could't find your balance. Please verify the address and try again."
        else:
            response = "Adress {} is not a valid Ethereum address.".format(address)
        return response