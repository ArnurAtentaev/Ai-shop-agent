from pydantic import ConfigDict

from src.database_api.products.base_schemas import (
    ProductBase,
    ProductEmbeddingBase,
    CategoryBase,
    BrandBase,
    ProductInShopBase,
)


class ProductGet(ProductBase):
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    brand_id: int
    shop_id: int


class ProductEmbeddingGet(ProductEmbeddingBase):
    model_config = ConfigDict(from_attributes=True)


class ProductEmbeddingCreate(ProductEmbeddingBase):
    pass


class CategoryGet(CategoryBase):
    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(CategoryBase):
    pass


class BrandGet(BrandBase):
    model_config = ConfigDict(from_attributes=True)


class BrandCreate(BrandBase):
    pass


class GetProductInShop(ProductInShopBase):
    model_config = ConfigDict(from_attributes=True)
