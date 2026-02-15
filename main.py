import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.agent.graph import build_graph, gen_png_graph
from src.core.models import Base, db_helper
from src.agent.views import agent_router
from src.database_api import router as router_actions


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    with open("src/agent/intents.json") as f:
        app.state.intents = json.load(f)

    app.state.agent_graph = await build_graph(intents=app.state.intents)
    gen_png_graph(app.state.agent_graph, name_photo="main_graph.png")

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_actions, prefix="/creating_actions")
app.include_router(router=agent_router, prefix="/agent")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
