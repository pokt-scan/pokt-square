# pocket-ai-agent

## Build

1. Generate docker image running on root folder:

```bash
./build.sh
```

## Run with docker-compose

**NOTE** By default, the docker is attached into the "host" network

1. A simple docker-compose is provided. It requires only to wirte a `.env` file with 

```bash
OPENAI_API_KEY= <YOUR_OPENAI_API_KEY>
POCKET_NEWTWORK_ETH_URL=<VALID_ETH_ENDPOINT>
```
2. Run on root folder 

```bash
docker compose up
```

3. Interact! using Python as example:

```python
import requests
address = "<ETH_ADDRESS>"
inputs = {"input": {"input": f"What is the balance of the  ETH address {address}?"}}
response = requests.post("http://localhost:8080/pocket_agent/invoke", json=inputs)
response.json()
```

# Tools

At the moment, only the method `get_balance` for the Eth blockchains is writen as an example. Probably more chains would be added. Each blockchain would require to have its own set of Langchain `Tools` developed. Moreover, it can be written one agent specialized by blockchain, and then each agent be consolidated as a tool of a more general agent.
