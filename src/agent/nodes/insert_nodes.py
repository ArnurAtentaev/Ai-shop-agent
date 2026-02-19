import logging

from agent.states import OverallAgentState
from agent.prompts import (
    INSERT_ORDER_REPORT_PROMPT,
    INSERT_CONFIRM_NODE,
)

from langchain_core.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO)


def insert_confirm_node(state: OverallAgentState, models) -> OverallAgentState:
    prompt = PromptTemplate(
        input_variables=["question", "intent", "order_products", "city"],
        template=INSERT_CONFIRM_NODE,
    )

    llm_chain = prompt | models["generative_model"]
    result = llm_chain.invoke(
        {
            "question": state.query,
            "intent": state.intent_result,
            "order_products": state.tool_res,
            "city": state.slots["city"],
        }
    )

    logging.info("IT IS INSERT CONFIRM NODE")

    state.waiting_confirmation = True
    state.answer = result.content
    return state


def insert_report_node(state: OverallAgentState, models) -> OverallAgentState:
    prompt = PromptTemplate(
        input_variables=["data"], template=INSERT_ORDER_REPORT_PROMPT
    )

    llm_chain = prompt | models["generative_model"]

    result = llm_chain.invoke(
        {
            "data": state.tool_res,
        }
    )

    state.waiting_confirmation = False
    state.confirmation_status = "stop"
    state.answer = result.content
    logging.info(f"INSERT REPORT RESULT: {state.answer}")
    return state
