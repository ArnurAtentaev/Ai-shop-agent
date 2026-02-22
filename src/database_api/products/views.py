from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database_api.products.schemas import (
    BrandCreate,
    BrandGet,
    ProductGet,
    ProductCreate,
    CategoryGet,
    CategoryCreate,
)
from core.models import db_helper
from database_api.products import crud


router_product = APIRouter(tags=["Products"])


@router_product.post(
    "/product",
    response_model=ProductGet,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreate,
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(
        session=session, product_in=product_in, models=request.app.state.models
    )


@router_product.post(
    "/category", response_model=CategoryGet, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_categories(session=session, category_in=category_in)


@router_product.post(
    "/brand", response_model=BrandGet, status_code=status.HTTP_201_CREATED
)
async def create_brand(
    brand_in: BrandCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_brands(session=session, brand_in=brand_in)
