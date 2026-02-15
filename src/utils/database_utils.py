import logging

from decimal import Decimal
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import select, func

from src.agent.initialize_models import reranker_model
from src.core.models.shop import Ratings

logging.basicConfig(level=logging.INFO)


def build_product_text(
    name: str,
    category: str,
    brand: str,
    shop: str,
    price: Decimal,
    characteristics: dict,
) -> str:
    characteristics_text = "\n".join(f"- {k}: {v}" for k, v in characteristics.items())
    return f"""
            Product: {name}
            Category: {category}
            Brand: {brand}
            Shop: {shop}
            Price: {price}
            Characteristics:
            {characteristics_text}
            """.strip()


def chunking(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
    )
    return splitter.split_text(text)


def reranker(query: str, found, top_n: int = 1):
    pairs = [(query, text) for text in found]

    scores = reranker_model.predict(pairs)
    logging.info(f"RERANKER SCORES: {scores}")

    reranked = list(zip(found, scores))
    top_filtered = sorted(reranked, key=lambda x: x[1], reverse=True)
    logging.info(f"RERANKED: {top_filtered}")

    return [p for p, _ in top_filtered[:top_n]]


def format_characteristics(characteristic: dict) -> str:
    if not characteristic:
        return "Нет характеристик."
    lines = [f"- {key}: {value}" for key, value in characteristic.items()]
    return "\n".join(lines)


def format_sql_results(data, rating: bool = False):
    result = []
    for product in data:
        if rating:
            product["shop_rating_avg"] = (
                float(product["shop_rating_avg"])
                if product["shop_rating_avg"] is not None
                else "У магазина отсутствует рейтинг"
            )
        result.append(product)
    return result


def rating_subquery():
    ratings_subq = (
        select(
            Ratings.shop_id,
            func.round(func.avg(Ratings.scores), 2).label("shop_rating_avg"),
        )
        .group_by(Ratings.shop_id)
        .subquery()
    )
    return ratings_subq
