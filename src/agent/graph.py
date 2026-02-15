from pathlib import Path
from functools import partial

from .states import OverallAgentState
from .nodes.common_nodes import (
    intent_classification,
    confirmation_parser_node,
    intent_dispatcher,
    ner_slots_classification_node,
    ask_missing_slots_node,
    language_adaptation_node,
)
from .routers import (
    start_router,
    intent_router,
    query_intent_router,
    insert_router,
    tools_classification_router,
)
from .nodes.insert_nodes import insert_report_node
from .nodes.crud_nodes import tool_make_order
from .subgraphs.subgraphs import (
    search_nodes_subgraph,
    insert_nodes_subgraph,
    general_actions_subgraph,
)

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()


def gen_png_graph(app_obj, name_photo: str, folder: str = "graph_images") -> None:
    save_dir = Path(folder)
    save_dir.mkdir(parents=True, exist_ok=True)
    file_path = save_dir / name_photo

    with open(file_path, "wb") as f:
        f.write(app_obj.get_graph().draw_mermaid_png())


async def build_graph(intents):
    workflow = StateGraph(OverallAgentState)

    gen_png_graph(search_nodes_subgraph(), name_photo="search_subgraph.png")
    gen_png_graph(insert_nodes_subgraph(), name_photo="insert_subgraph.png")
    gen_png_graph(general_actions_subgraph(), name_photo="general_actions_subgraph.png")
    search_subgraph = search_nodes_subgraph()
    insert_subgraph = insert_nodes_subgraph()
    general_subgraph = general_actions_subgraph()

    workflow.add_node("intent", partial(intent_classification, intents=intents))
    workflow.add_node("intent_dispatcher", intent_dispatcher)
    workflow.add_node("ner", partial(ner_slots_classification_node, intents=intents))

    workflow.add_node("ask_missing_slots", ask_missing_slots_node)
    workflow.add_node("search_subgraph", search_subgraph)
    workflow.add_node("insert_subgraph", insert_subgraph)
    workflow.add_node("general_subgraph", general_subgraph)

    workflow.add_node("tool_make_order", tool_make_order)

    workflow.add_node("confirm_parser", confirmation_parser_node)

    workflow.add_node("language_adaptation_node", language_adaptation_node)
    workflow.add_node("insert_report_node", insert_report_node)

    workflow.add_conditional_edges(
        START,
        start_router,
        {
            "intent": "intent",
            "confirm": "confirm_parser",
        },
    )
    workflow.add_conditional_edges(
        "intent",
        query_intent_router,
        {
            "did_not_classify": "intent_dispatcher",
            "classified": "intent_dispatcher",
        },
    )
    workflow.add_conditional_edges(
        "intent_dispatcher",
        intent_router,
        {
            "slots": "ner",
            "general_actions": "general_subgraph",
            "did_not_classify": "language_adaptation_node",
        },
    )

    workflow.add_conditional_edges(
        "ner",
        tools_classification_router,
        {
            "ask_missing_slots": "ask_missing_slots",
            "search_tools": "search_subgraph",
            "insert_tools": "insert_subgraph",
        },
    )

    workflow.add_conditional_edges(
        "confirm_parser",
        insert_router,
        {
            "yes": "tool_make_order",
            "stop": "language_adaptation_node",
            "other": "language_adaptation_node",
        },
    )
    workflow.add_edge("tool_make_order", "insert_report_node")

    workflow.add_edge("ask_missing_slots", "language_adaptation_node")
    workflow.add_edge("search_subgraph", "language_adaptation_node")
    workflow.add_edge("insert_subgraph", "language_adaptation_node")
    workflow.add_edge("general_subgraph", "language_adaptation_node")
    workflow.add_edge("insert_report_node", "language_adaptation_node")

    workflow.add_edge("language_adaptation_node", END)
    return workflow.compile(checkpointer=checkpointer)
