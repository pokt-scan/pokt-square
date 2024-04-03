from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from packages.pocket_agent.agent import get_agent

app = FastAPI()

# Create agents, each will be working in different endpoints
pocket_agent = get_agent()
pocket_agent_openAPI = get_agent(USE_OPEN_API=True)


# Assign routes

# On root display docs
@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Add a route for each agent to feature
add_routes(app, pocket_agent, path="/pocket_agent")
add_routes(app, pocket_agent_openAPI, path="/pocket_agent_openAPI")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
