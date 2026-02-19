from typing import TYPE_CHECKING

from core.models.base import Base
from core.models.mixins import ShopRelationMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint

if TYPE_CHECKING:
    from .product import Product


class Shop(Base):
    __tablename__ = "shops"

    name: Mapped[str]
    city: Mapped[str]

    products: Mapped["Product"] = relationship(back_populates="shop")
    ratings: Mapped["Ratings"] = relationship(back_populates="shop")


class Ratings(ShopRelationMixin, Base):
    __tablename__ = "ratings"
    __table_args__ = (
        CheckConstraint("scores >= 1 AND scores <= 5", name="check_rating_range"),
    )

    _shop_back_populates = "ratings"

    scores: Mapped[int] = mapped_column(default=0.0)
