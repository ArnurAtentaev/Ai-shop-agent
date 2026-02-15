from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .product import Product
    from .shop import Shop


class ProductRelationMixin:
    _product_back_populates: str | None = None
    _product_id_nullable = False

    @declared_attr
    def product_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("products.id", ondelete="CASCADE"),
            nullable=cls._product_id_nullable,
        )

    @declared_attr
    def product(cls) -> Mapped["Product"]:
        return relationship(
            "Product",
            back_populates=cls._product_back_populates,
        )


class ShopRelationMixin:
    _shop_back_populates: str | None = None

    @declared_attr
    def shop_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("shops.id", ondelete="CASCADE"),
        )

    @declared_attr
    def shop(cls) -> Mapped["Shop"]:
        return relationship(
            "Shop",
            back_populates=cls._shop_back_populates,
        )
