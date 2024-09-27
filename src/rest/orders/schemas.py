from pydantic import BaseModel

from src.domain.entities.order import OrderStatus

from src.domain.entities.order_item import OrderItem


class CreateOrderRequestSchema(BaseModel):
    status: OrderStatus = OrderStatus.IN_PROCESS
    items: list[OrderItem] | None


class GetOrderResponseSchema(BaseModel):
    status: OrderStatus | None 
    items: list[OrderItem] | None
    