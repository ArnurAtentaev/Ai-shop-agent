import logging

from src.agent.states import OverallAgentState
from src.database_api.orders.schemas import CreateInsertOrder
from src.database_api.answers_to_questions.agent_crud import get_general_answer
from src.database_api.orders.agent_crud import get_orders, create_order
from src.database_api.products.agent_crud import (
    find_products,
    find_similar,
    get_product_by_article,
)

logging.basicConfig(level=logging.INFO)


async def tool_find_product(state: OverallAgentState) -> OverallAgentState:
    product_name = state.slots.get("product_name")

    result = await find_products.ainvoke(
        {
            "product_name": product_name,
        }
    )
    if not result:
        state.availability = False
        return state

    state.tool_res = result
    state.availability = True
    return state


async def tool_find_similar(state: OverallAgentState) -> OverallAgentState:
    product_name = state.slots.get("product_name")
    query = f"{product_name} {state.query}"

    result = await find_similar.ainvoke({"query": query})

    if not result:
        state.availability = False
        return state

    state.tool_res = result
    state.availability = True
    return state


async def tool_check_availability(
    state: OverallAgentState,
) -> OverallAgentState:
    data = CreateInsertOrder(
        articles=state.slots["articles"],
        quantity=state.slots["quantity"],
    )

    products = await get_product_by_article.ainvoke({"data": data})

    product_map = {p.article: p for p in products}
    errors = []

    for article, quantity in zip(data.articles, data.quantity):
        product = product_map.get(article)

        if not product:
            errors.append(f"Product with product {article} not found")
            continue

        if product.quantity < quantity:
            errors.append(
                f"Product {article}: available {product.quantity}, requested {quantity}"
            )

    logging.info(f"ERRORS AVAILABILITY: {errors}")

    if errors:
        state.tool_res = errors
        state.availability = False
        return state

    state.availability = True
    return state


async def tool_get_products_by_article(state: OverallAgentState) -> OverallAgentState:
    data = CreateInsertOrder(
        articles=state.slots["articles"],
        quantity=state.slots["quantity"],
    )

    products = await get_product_by_article.ainvoke(
        {"data": data, "for_update": False, "load_shop": True}
    )

    product_map = {p.article: p for p in products}

    products_list = []
    for idx, article in enumerate(state.slots["articles"]):
        p = product_map.get(article)
        quantity = state.slots["quantity"][idx]
        products_list.append(
            {
                "article": p.article,
                "product": p.name,
                "price": int(p.price),
                "quantity": quantity,
                "shop": p.shop.name,
            }
        )

    logging.info(f"CHECK PRODUCTS BY ARTICLE: {products_list}")
    return state


async def tool_make_order(state: OverallAgentState) -> OverallAgentState:
    data = CreateInsertOrder(
        articles=state.slots["articles"],
        quantity=state.slots["quantity"],
    )
    logging.info(f"DATA FOR ORDER: {data}")

    products = await get_product_by_article.ainvoke(
        {"data": data, "for_update": True, "load_shop": False}
    )
    await create_order.ainvoke(
        {
            "city": state.slots["city"],
            "items": data,
            "products": products,
        }
    )

    return state


async def tool_get_orders(state: OverallAgentState) -> OverallAgentState:
    result = await get_orders.ainvoke({})

    if not result:
        state.answer = "You do not have orders."
    else:
        state.tool_res = result
    return state


async def tool_general_questions(state: OverallAgentState) -> OverallAgentState:
    state.tool_res = None
    result = await get_general_answer.ainvoke({"query": state.query})

    if not result:
        return state

    state.answer = result
    return state
