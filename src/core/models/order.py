from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, Integer
from sqlalchemy.schema import Sequence

from core.models.base import Base

if TYPE_CHECKING:
    from .order_associate import OrderAssociation


class Order(Base):
    __tablename__ = "orders"

    order_number_seq = Sequence("order_number_seq", increment=1, start=1, cycle=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    delivery_to_city: Mapped[str]
    order_number: Mapped[int] = mapped_column(
        Integer,
        order_number_seq,
        server_default=order_number_seq.next_value(),
        unique=True,
        nullable=False,
    )

    products_details: Mapped[list["OrderAssociation"]] = relationship(
        back_populates="order"
    )
