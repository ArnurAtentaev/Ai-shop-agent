import logging

from fastapi import APIRouter, Request
from .schemas import AgentResponse, APIResponse

logging.basicConfig(level=logging.INFO)

agent_router = APIRouter()


@agent_router.post("/", response_model=APIResponse)
async def ai_agent_chat(request: Request, query: str):
    agent_graph = request.app.state.agent_graph

    config = {"configurable": {"thread_id": "user_42"}}
    state = await agent_graph.ainvoke({"query": query}, config=config)

    response = AgentResponse(
        tool_res=state.get("tool_res", None), answer=state["answer"]
    )
    logging.info(f"RESPONSE: {response.model_dump()}")
    return {"response": response}
