import logging

from core.models.db import db_helper
from core.models import Product, Order, OrderAssociation, Shop

from langchain_core.tools import tool
from .schemas import OrderItemBase

from sqlalchemy import select, update
from sqlalchemy.exc import OperationalError

logging.basicConfig(level=logging.INFO)


@tool
async def get_orders():
    """Get user orders."""

    session = db_helper.get_scoped_session()

    try:
        stmt = (
            select(
                Order.order_number,
                Order.delivery_to_city,
                Product.name.label("product_name"),
                Product.article,
                Shop.name,
                OrderAssociation.quantity,
                OrderAssociation.price,
            )
            .join(OrderAssociation, OrderAssociation.order_id == Order.id)
            .join(Product, Product.id == OrderAssociation.product_id)
            .join(Shop, Shop.id == Product.shop_id)
            .limit(2)
        )
        exec = await session.execute(stmt)
        result_execution = exec.mappings().all()
        logging.info(f"GET ORDERS: {result_execution}")

        result = [dict(row) for row in result_execution]

        return result

    except OperationalError as oper_error:                                                                                                          
        logging.exception(f"DB error in get_orders: {oper_error}")

    finally:
        await session.close()


@tool
async def create_order(city, items, products):
    """Make order."""

    session = db_helper.get_scoped_session()

    try:
        product_map = {p.article: p for p in products}

        order_items = []

        for article, requested_quantities in zip(items.articles, items.quantity):
            product = product_map.get(article)
            order_items.append(
                OrderItemBase(
                    product_id=product.id,
                    quantity=requested_quantities,
                    price=product.price,
                )
            )

        order = Order(delivery_to_city=city)

        for item in order_items:
            order.products_details.append(
                OrderAssociation(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                )
            )
            up_stmt = (
                update(Product)
                .where(Product.id == item.product_id)
                .values(quantity=Product.quantity - item.quantity)
            )
            await session.execute(up_stmt)

        session.add(order)
        await session.commit()

    except OperationalError as oper_error:
        logging.exception(f"DB error in create_order: {oper_error}")

    finally:
        await session.close()
