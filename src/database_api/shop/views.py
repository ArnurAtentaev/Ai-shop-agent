from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database_api.shop.schemas import (
    GetRatingShop,
    CreateRatingShop,
    GetShop,
    CreateShop,
)
from core.models import db_helper
from database_api.shop import crud


router_shop = APIRouter(tags=["Shop"])


@router_shop.post(
    "/",
    response_model=GetShop,
    status_code=status.HTTP_201_CREATED,
)
async def create_shops(
    shop_in: CreateShop,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_shop(
        session=session,
        shop_in=shop_in,
    )


@router_shop.post(
    "/rating",
    response_model=GetRatingShop,
    status_code=status.HTTP_201_CREATED,
)
async def create_rating_for_shops(
    rating_in: CreateRatingShop,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_rating(
        session=session,
        rating_in=rating_in,
    )
