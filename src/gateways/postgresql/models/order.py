import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.gateways.postgresql.models.base import BaseORM
from src.gateways.postgresql.models.mixins import UpdatedAtMixin, UUIDOidMixin

from src.domain.entities.order import Order, OrderStatus

from src.gateways.postgresql.models.order_item import OrderItemORM

OrderStatusType: sa.Enum = sa.Enum(
    OrderStatus,
    name="order_status",
    create_constraint=True,
    metadata=BaseORM.metadata,
    validate_strings=True,
)


class OrderORM(BaseORM, UUIDOidMixin, UpdatedAtMixin):
    __tablename__ = "orders"

    status: Mapped[OrderStatus] = mapped_column(nullable=False)
    items: Mapped[list[OrderItemORM]] = relationship(
        "OrderItemORM", back_populates="order",
        cascade="all, delete-orphan"
    )

    @staticmethod
    def from_entity(entity: Order) -> "OrderORM":
        return OrderORM(
            oid=entity.oid, status=entity.status
        )

    @staticmethod
    def to_entity(self) -> Order:
        return Order(
            oid=self.oid, 
            status=self.status,
            items=[OrderItemORM.to_entity(item) for item in self.items]
        )
