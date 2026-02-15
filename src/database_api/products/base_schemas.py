from typing import Dict, Union, Literal, Optional

from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.utils.pydantic_validators import capitalize_str


class ProductBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    characteristic: Dict[str, Union[str, int, float]]
    price: Decimal = Field(ge=0.1, decimal_places=2, max_digits=12)
    currency: Literal["KZT", "USD", "RUB"] = "KZT"
    quantity: int = Field(ge=0, default=0)

    @field_validator("name", mode="before")
    def validate_name(cls, value: str):
        return capitalize_str(value)


class ProductEmbeddingBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_text: str
    embedding: list[float]


class CategoryBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str

    @field_validator("name", mode="before")
    def validate_name(cls, value: str):
        return capitalize_str(value)


class BrandBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str

    @field_validator("name", mode="before")
    def validate_name(cls, value: str):
        return capitalize_str(value)


class ProductInShopBase(BaseModel):
    product_name: str
    article: int
    price: float
    characteristic: Dict[str, str]

    shop_name: str
    shop_city: str
    shop_rating_avg: Optional[float] = None
