from typing import Optional, Dict, List, Any, Literal

from pydantic import BaseModel


class OverallAgentState(BaseModel):
    query: str
    intent_result: Optional[str] = None
    slots: Optional[Dict] = None
    tool_res: Optional[List[Dict[str, Any] | str]] = None
    relevant: Optional[str] = None
    answer: Optional[Dict | str | List] = None

    waiting_confirmation: Optional[bool] = None
    confirmation_status: Literal["yes", "stop", "other"] | None = None
    availability: bool | None = None
