import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass


from src.domain.entities.order import Order
from src.gateways.postgresql.repositories.order import IOrderRepository


class IOrderService(ABC): 
    @abstractmethod
    async def create_order(self, order_data: Order) -> Order:
        pass



@dataclass
class OrderService(IOrderService):
    repository: IOrderRepository

    async def create_order(self, order_data: Order) -> Order:
        order = repository.create(order_data)
        return order