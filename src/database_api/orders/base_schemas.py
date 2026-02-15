from typing import List
from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class InsertOrderBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    articles: list[int]
    quantity: list[int]


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: Decimal


class OrderBase(BaseModel):
    product_name: str
    article: int
    quantity: int
    price: Decimal


class OrdersBase(BaseModel):
    order_number: int
    delivery_to_city: str
    product_name: str
    items: List[OrderBase]
