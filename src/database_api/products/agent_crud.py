import logging
from typing import Optional

from src.core.models.db import db_helper
from src.database_api.orders.schemas import CreateInsertOrder
from src.agent.initialize_models import embedding_model
from src.utils.database_utils import rating_subquery, format_sql_results
from src.core.models import Product, Shop, ProductEmbedding
from .schemas import ProductEmbeddingGet

from langchain_core.tools import tool
from sqlalchemy.orm import joinedload
from sqlalchemy import FLOAT, select, cast
from sqlalchemy.exc import SQLAlchemyError, OperationalError

logging.basicConfig(level=logging.INFO)


@tool
async def find_products(product_name: str) -> Optional[Product]:
    """Sql query to find and get products, what person chose."""

    session = db_helper.get_scoped_session()
    try:
        ratings_subq = rating_subquery()

        stmt_product = (
            select(
                Product.name.label("product_name"),
                Product.price,
                Product.article,
                Product.characteristic,
                Shop.name.label("shop_name"),
                Shop.city.label("shop_city"),
                ratings_subq.c.shop_rating_avg,
            )
            .join(Shop, Shop.id == Product.shop_id)
            .outerjoin(ratings_subq, ratings_subq.c.shop_id == Shop.id)
            .where(Product.name.ilike(f"%{product_name}%"))
            .limit(3)
        )

        exec = await session.execute(stmt_product)
        result_execution = exec.mappings().all()

        logging.info(f"RESULT EXEC DB: {result_execution}")

        if not result_execution:
            return None

        to_dict = [dict(row) for row in result_execution]
        result = format_sql_results(to_dict, rating=True)

        return result

    except SQLAlchemyError as sqlerror:
        logging.exception(f"DB error in find_products: {sqlerror}")

    finally:
        await session.close()


@tool
async def find_similar(
    query: str, k_similarity: int = 10, limit: int = 3
) -> Optional[list[ProductEmbeddingGet]]:
    """Sql query to find similar products."""

    query_vector = embedding_model.encode(
        query,
        normalize_embeddings=True,
    )
    session = db_helper.get_scoped_session()

    try:
        distance = cast(ProductEmbedding.embedding.op("<=>")(query_vector), FLOAT)
        subq_distance = (
            select(
                ProductEmbedding.product_id,
                distance.label("distance"),
            )
            .where(distance < 0.5)
            .order_by(distance)
            .limit(k_similarity)
            .subquery()
        )

        ratings_subq = rating_subquery()

        stmt_products = (
            select(
                Product.name.label("product_name"),
                Product.price,
                Product.article,
                Product.characteristic,
                Shop.name.label("shop_name"),
                Shop.city.label("shop_city"),
                ratings_subq.c.shop_rating_avg,
            )
            .join(subq_distance, subq_distance.c.product_id == Product.id)
            .join(Shop, Shop.id == Product.shop_id)
            .outerjoin(ratings_subq, ratings_subq.c.shop_id == Shop.id)
            .distinct(Product.id)
            .limit(limit)
        )
        exec = await session.execute(stmt_products)
        result_execution = exec.mappings().all()

        if not result_execution:
            logging.info("DID NOT FIND ANY PRODUCTS")
            return None

        to_dict = [dict(row) for row in result_execution]
        result = format_sql_results(to_dict, rating=True)
        logging.info(f"{result}")

        return result

    except SQLAlchemyError as sqlerror:
        logging.exception(f"DB error in find_similar: {sqlerror}")

    finally:
        await session.close()


@tool
async def get_product_by_article(
    data: CreateInsertOrder,
    for_update: bool = False,
    load_shop: bool = False,
):
    """Get product/s by article/s."""

    session = db_helper.get_scoped_session()

    try:
        stmt = select(Product).where(Product.article.in_(data.articles))
        if load_shop is True:
            stmt = stmt.options(joinedload(Product.shop))

        if for_update is True:
            stmt = stmt.with_for_update()

        exec = await session.execute(stmt)
        result_execution = exec.scalars().all()
        logging.info(f"GET PRODUCT BY ARTICLE: {result_execution}")

        return result_execution

    except OperationalError as oper_error:
        logging.exception(f"DB error in check_product_by_article: {oper_error}")

    finally:
        await session.close()
