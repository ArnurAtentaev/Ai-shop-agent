from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from src.core.models.base import Base

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderAssociation(Base):
    __tablename__ = "order_associations"

    __table_args__ = (
        UniqueConstraint("product_id", "order_id", name="idx_unique_order_product"),
    )

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1, server_default="1")
    price: Mapped[int] = mapped_column(default=0, server_default="0")

    product: Mapped["Product"] = relationship(back_populates="orders_details")
    order: Mapped["Order"] = relationship(back_populates="products_details")
