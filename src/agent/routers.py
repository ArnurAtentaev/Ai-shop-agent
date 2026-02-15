from src.agent.states import OverallAgentState

from src.agent.states_variables import (
    SLOT_INTENTS,
    GENERAL_ACTION_INTENTS,
    SEARCH_TOOLS,
    INSERT_TOOLS,
)


def start_router(state: OverallAgentState) -> str:
    if state.waiting_confirmation:
        return "confirm"
    return "intent"


def query_intent_router(state: OverallAgentState) -> str:
    if not state.intent_result:
        return "did_not_classify"
    else:
        return "classified"


def intent_router(state: OverallAgentState) -> str:
    intent = state.intent_result

    if intent in SLOT_INTENTS:
        return "slots"
    elif intent in GENERAL_ACTION_INTENTS:
        return "general_actions"
    else:
        return "did_not_classify"


def tools_classification_router(state: OverallAgentState) -> str:
    if not state.slots or any(
        (v is None) or (isinstance(v, list) and len(v) == 0)
        for v in state.slots.values()
    ):
        return "ask_missing_slots"

    if state.intent_result in SEARCH_TOOLS:
        return "search_tools"

    elif state.intent_result in INSERT_TOOLS:
        return "insert_tools"


def tools_router(state: OverallAgentState) -> str:
    if state.intent_result != "make_order":
        return f"{state.intent_result}"

    return "make_order"


def insert_router(state: OverallAgentState) -> str:
    return state.confirmation_status


def check_relevants_router(state: OverallAgentState) -> str:
    """Checking the relevance of the conclusion"""

    if state.tool_res is None:
        return "does not fit"
    return "fit"


def availability_router(state: OverallAgentState) -> str:
    if state.availability is True:
        return "available"

    return "not_available"


def general_answer_base_router(state: OverallAgentState) -> str:
    if state.tool_res:
        return "tool_result"

    if state.answer:
        return "answer"
    return "does_not_answer"


def general_actions_router(state: OverallAgentState) -> str:
    return f"{state.intent_result}"
