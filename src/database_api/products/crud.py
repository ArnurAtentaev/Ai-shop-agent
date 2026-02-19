import logging

from core.models import Product, ProductEmbedding, Category, Brand, Shop
from database_api.products.schemas import BrandCreate, ProductCreate, CategoryCreate
from utils.database_utils import build_product_text, chunking

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

logging.basicConfig(level=logging.INFO)


async def create_product(session: AsyncSession, product_in: ProductCreate, models):
    category = await session.get(Category, product_in.category_id)
    if not category:
        raise HTTPException(404, "Category not found")

    brand = await session.get(Brand, product_in.brand_id)
    if not brand:
        raise HTTPException(404, "Brand not found")
    shop = await session.get(Shop, product_in.shop_id)

    product_dict = product_in.model_dump(exclude={"article"})
    product = Product(**product_dict)

    session.add(product)
    await session.flush()

    product_text = build_product_text(
        name=product.name,
        category=category.name,
        brand=brand.name,
        shop=shop.name,
        price=product.price,
        characteristics=product.characteristic,
    )
    logging.info(f"BUILDED TEXT: {product_text}")

    chunks = chunking(product_text)
    embeddings = models["embedding_model"].encode(chunks)

    for chunk, vector in zip(chunks, embeddings):
        session.add(
            ProductEmbedding(
                product_id=product.id,
                chunk_text=chunk,
                embedding=vector.tolist(),
            )
        )

    await session.commit()
    return product


async def create_categories(session: AsyncSession, category_in: CategoryCreate):
    category_dict = category_in.model_dump()
    category = Category(**category_dict)

    session.add(category)
    await session.commit()

    return category


async def create_brands(session: AsyncSession, brand_in: BrandCreate):
    brand_dict = brand_in.model_dump()
    brand = Brand(**brand_dict)

    session.add(brand)
    await session.commit()

    return brand
