# POKT Square - Building Elegant RAGs

![It's better than a RAG](./assets/pocket_square_diff_small.png)

This is a **WORK IN PROGRESS** proof of concept of Retrieval Augmented Generation agent based on [LanChain](https://www.langchain.com/) and deployed with [LangServe](https://www.langchain.com/langchain). 
The objective of this repository is to show how the Pocket Network can be used to access web3 data and language models.

## TO DO
- [Morse] Create functional OpenAPI tools.
- [Morse] Add Pocket Network LLM backends.
- [Shannon] Add decentralized access (using Pocket Apps)

## Build

1. Generate docker image running on root folder:

```bash
./build.sh
```


## Run with docker-compose

**NOTE** By default, the docker is attached into the "host" network

1. A simple docker-compose is provided. It requires only to write a `.env` file with 

```bash
OPENAI_API_KEY= <YOUR_OPENAI_API_KEY>
POCKET_NEWTWORK_ETH_URL=<VALID_ETH_ENDPOINT>
OPENAI_CHAT_MODEL=<OPEN_AI_CHAT_MODEL>
POCKET_NEWTWORK_ETH_OPEN_API_DOCS=<URL_OF_RAW_OPEN_API_SPEC>
```

An example of the last three parameters is:
```
POCKET_NEWTWORK_ETH_URL=https://eth-mainnet.rpc.pokt.dev/v1/
OPENAI_CHAT_MODEL=gpt-3.5-turbo
POCKET_NEWTWORK_ETH_OPEN_API_DOCS=https://raw.githubusercontent.com/pokt-foundation/grove-path/main/specs/eth/eth_getBalance.yaml
```

2. Run on root folder 

```bash
docker compose up
```

3. Interact! 

using Python as example:

```python
import requests
address = "<ETH_ADDRESS>"
inputs = {"input": {"input": f"What is the balance of the  ETH address {address}?"}}
response = requests.post("http://localhost:8080/pocket_agent/invoke", json=inputs)
response.json()
```

# Tools

At the moment, only the method `get_balance` for the Eth blockchains is available as an example. 

Feel free to code more tools and add them to this repository via pull requests!

Each blockchain (probably) necessitates its own dedicated suite of Langchain `Tools` to be developed. Furthermore, an efficient approach could involve crafting individual agents specialized for each blockchain, which could then be integrated into a more comprehensive agent as tools.
