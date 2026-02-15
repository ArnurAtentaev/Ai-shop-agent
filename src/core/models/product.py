from typing import TYPE_CHECKING

from .base import Base
from src.core.models.mixins import ProductRelationMixin, ShopRelationMixin

from pgvector.sqlalchemy import VECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Sequence
from sqlalchemy import Text, ForeignKey, DECIMAL, Numeric, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql.json import JSONB

if TYPE_CHECKING:
    from .order_associate import OrderAssociation


class Product(ShopRelationMixin, Base):
    __tablename__ = "products"

    _shop_back_populates = "products"
    __table_args__ = (
        CheckConstraint(
            "quantity >= 0",
            name="constraint_product_units",
        ),
    )

    article_seq = Sequence("article_seq", increment=1, start=100000, cycle=False)

    name: Mapped[str] = mapped_column()
    characteristic: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    price: Mapped[DECIMAL] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(default="KZT")
    article: Mapped[int] = mapped_column(
        Integer(),
        article_seq,
        server_default=article_seq.next_value(),
        unique=True,
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)

    orders_details: Mapped[list["OrderAssociation"]] = relationship(
        back_populates="product",
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
    )
    brand_id: Mapped[int] = mapped_column(
        ForeignKey(
            "brands.id",
            ondelete="CASCADE",
        )
    )

    embeddings: Mapped[list["ProductEmbedding"]] = relationship(
        back_populates="product",
    )
    category: Mapped["Category"] = relationship(back_populates="product")
    brand: Mapped["Brand"] = relationship(
        back_populates="product",
    )


class ProductEmbedding(ProductRelationMixin, Base):
    __tablename__ = "product_embeddings"

    _product_back_populates = "embeddings"

    chunk_text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(
        VECTOR(384),
    )


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str]

    product: Mapped["Product"] = relationship(back_populates="category")


class Brand(Base):
    __tablename__ = "brands"

    name: Mapped[str]

    product: Mapped["Product"] = relationship(back_populates="brand")
