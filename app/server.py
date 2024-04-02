from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from packages.pocket_agent.agent import agent as pocket_agent

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(app, pocket_agent, path="/pocket_agent")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
