from uuid import UUID
from enum import Enum
from dataclasses import dataclass, field


@dataclass
class OrderItem:
    oid: UUID | None = None
    order_id: UUID | None = None
    product_id: UUID | None = None
    """ Колличество товара в закаче """
    quantity: int = 0
    
