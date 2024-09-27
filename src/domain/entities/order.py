from uuid import UUID
from enum import Enum
from dataclasses import dataclass, field

from src.domain.entities.order_item import OrderItem


class OrderStatus(str, Enum):
    IN_PROCESS = "в процессе"
    SHIPPED = "отправлен"
    DELIVERED = "доставлен"


@dataclass
class Order:
    oid: UUID | None = None
    status: OrderStatus = OrderStatus.IN_PROCESS
    items: OrderItem | None = None 