from functools import partial

from agent.states import OverallAgentState
from agent.routers import (
    tools_router,
    availability_router,
    general_answer_base_router,
    general_actions_router,
)
from agent.nodes.crud_nodes import (
    tool_find_product,
    tool_find_similar,
    tool_check_availability,
    tool_get_products_by_article,
    tool_get_orders,
    tool_general_questions,
)
from agent.nodes.common_nodes import tool_base_answer_node, model_fallback_node
from agent.nodes.insert_nodes import insert_confirm_node

from langgraph.graph import StateGraph, START, END


def search_nodes_subgraph(models):
    search_sub_workflow = StateGraph(OverallAgentState)
    SEARCH_TOOLS = {
        "find_product": tool_find_product,
        "find_similar": partial(tool_find_similar, models=models),
    }

    for name, func in SEARCH_TOOLS.items():
        search_sub_workflow.add_node(name, func)

    search_sub_workflow.add_node(
        "base_answer_node", partial(tool_base_answer_node, models=models)
    )
    search_sub_workflow.add_node(
        "model_fallback", partial(model_fallback_node, models=models)
    )

    search_sub_workflow.add_conditional_edges(
        START, tools_router, {key: key for key in SEARCH_TOOLS.keys()}
    )

    for node in SEARCH_TOOLS.keys():
        search_sub_workflow.add_conditional_edges(
            node,
            availability_router,
            {"not_available": "model_fallback", "available": "base_answer_node"},
        )

    search_sub_workflow.add_edge("base_answer_node", END)
    search_sub_workflow.add_edge("model_fallback", END)

    return search_sub_workflow.compile()


def insert_nodes_subgraph(models):
    insert_sub_workflow = StateGraph(OverallAgentState)

    insert_sub_workflow.add_node("check_availability", tool_check_availability)
    insert_sub_workflow.add_node(
        "get_products_by_article", tool_get_products_by_article
    )
    insert_sub_workflow.add_node(
        "insert_confirm_node", partial(insert_confirm_node, models=models)
    )
    insert_sub_workflow.add_node(
        "model_fallback", partial(model_fallback_node, models=models)
    )

    insert_sub_workflow.add_edge(START, "check_availability")

    insert_sub_workflow.add_conditional_edges(
        "check_availability",
        availability_router,
        {"not_available": "model_fallback", "available": "get_products_by_article"},
    )

    insert_sub_workflow.add_edge("get_products_by_article", "insert_confirm_node")
    insert_sub_workflow.add_edge("insert_confirm_node", END)
    insert_sub_workflow.add_edge("model_fallback", END)

    return insert_sub_workflow.compile()


def general_actions_subgraph(models):
    general_sub_workflow = StateGraph(OverallAgentState)

    GENERAL_TOOLS = {
        "get_orders": tool_get_orders,
        "general_question": partial(tool_general_questions, models=models),
    }

    for name, func in GENERAL_TOOLS.items():
        general_sub_workflow.add_node(name, func)

    general_sub_workflow.add_node(
        "base_answer_node", partial(tool_base_answer_node, models=models)
    )
    general_sub_workflow.add_node(
        "model_fallback", partial(model_fallback_node, models=models)
    )

    general_sub_workflow.add_conditional_edges(
        START, general_actions_router, {key: key for key in GENERAL_TOOLS.keys()}
    )

    for node in GENERAL_TOOLS.keys():
        general_sub_workflow.add_conditional_edges(
            node,
            general_answer_base_router,
            {
                "does_not_answer": "model_fallback",
                "tool_result": "base_answer_node",
                "answer": END,
            },
        )

    general_sub_workflow.add_edge("base_answer_node", END)
    general_sub_workflow.add_edge("model_fallback", END)

    return general_sub_workflow.compile()
