import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError

from core.models.shop import Shop, Ratings
from .schemas import CreateRatingShop, CreateShop

logging.basicConfig(level=logging.INFO)


async def create_shop(session: AsyncSession, shop_in: CreateShop):
    shop_dict = shop_in.model_dump()
    shop = Shop(**shop_dict)

    session.add(shop)
    await session.commit()
    return shop


async def create_rating(session: AsyncSession, rating_in: CreateRatingShop):
    rating_dict = rating_in.model_dump()
    rating = Ratings(**rating_dict)

    try:
        session.add(rating)
        await session.commit()
    except OperationalError as session_error:
        logging.error(f"Could not insert rating for shop: {session_error}")
        await session.rollback()
    finally:
        await session.close()
    return rating
