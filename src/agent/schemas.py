from pydantic import BaseModel
from typing import Optional, List, Any


class AgentResponse(BaseModel):
    tool_res: Optional[List[Any]] = None
    answer: str


class APIResponse(BaseModel):
    response: AgentResponse
