import uuid
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.gateways.postgresql.models.base import BaseORM
from src.gateways.postgresql.models.mixins import UpdatedAtMixin, UUIDOidMixin

from src.domain.entities.order_item import OrderItem


class OrderItemORM(BaseORM, UUIDOidMixin, UpdatedAtMixin):
    __tablename__ = "order_items"

    oid: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), sa.ForeignKey("orders.oid"), nullable=False
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), sa.ForeignKey("products.oid"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)

    order: Mapped["OrderORM"] = relationship("OrderORM", back_populates="items")
    product: Mapped["ProductORM"] = relationship(
        "ProductORM", back_populates="order_items"
    )

    @staticmethod
    def from_entity(entity: OrderItem) -> "OrderItemORM":
        return OrderItemORM(
            oid=entity.oid,
            order_id=entity.order_id,
            product_id=entity.product_id,
            quantity=entity.quantity,
        )

    @staticmethod
    def to_entity(self) -> OrderItem:
        return OrderItem(
            oid=self.oid,
            order_id=self.order_id,
            product_id=self.product_id,
            quantity=self.quantity,
        )
