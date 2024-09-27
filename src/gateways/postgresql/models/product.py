import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.domain.entities.product import Product
from src.gateways.postgresql.models.base import BaseORM
from src.gateways.postgresql.models.mixins import UpdatedAtMixin, UUIDOidMixin

from src.gateways.postgresql.models.order_item import OrderItemORM

class ProductORM(BaseORM, UUIDOidMixin, UpdatedAtMixin):
    __tablename__ = "products"

    title: Mapped[str | None] = mapped_column(sa.String(128))
    description: Mapped[str | None] = mapped_column(sa.VARCHAR(255))
    price: Mapped[float | None] = mapped_column(sa.Float())
    quantity: Mapped[int | None] = mapped_column(sa.Integer())

    order_items: Mapped[list[OrderItemORM]] = relationship(
        "OrderItemORM", back_populates="product"
    )

    @staticmethod
    def from_entity(entity: Product) -> "ProductORM":
        return ProductORM(
            oid=entity.oid,
            title=entity.title,
            price=entity.price,
            description=entity.description,
            quantity=entity.quantity,
        )

    @staticmethod
    def to_entity(self) -> Product:
        return Product(
            oid=self.oid,
            title=self.title,
            price=self.price,
            description=self.description,
            quantity=self.quantity,
        )
