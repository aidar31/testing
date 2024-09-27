import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.domain.entities.order import Order
from src.domain.entities.order_item import OrderItem

from src.gateways.postgresql.database import Database
from src.gateways.postgresql.models.order import OrderORM
from src.gateways.postgresql.models.order_item import OrderItemORM



class IOrderRepository(ABC):
    @abstractmethod
    async def get_by_oid(self, oid: uuid.UUID) -> OrderORM | None:
        pass

    @abstractmethod
    async def create(self, order_data: Order) -> OrderORM:
        pass

    @abstractmethod
    async def add_item(self, item_data: OrderItem) -> bool:
        pass

@dataclass
class ORMOrderRepository(IOrderRepository):
    database: Database

    async def get_by_oid(self, oid: uuid.UUID) -> OrderORM | None:
        stmt = select(OrderORM).where(OrderORM.oid == oid).limit(1)
        async with self.database.get_read_only_session() as session:
            return await session.scalar(stmt)

    async def create(self, order_data: Order) -> OrderORM: 
        order_orm = OrderORM.from_entity(order_data)
        items_orm = [OrderItemORM.from_entity(item) for item in order_data.items]

        async with self.database.get_session() as session: 
            session.add(order_orm)

            for item in items_orm:
                session.add(item)

        return order_orm
    
    async def add_item(self, item_data: OrderItem) -> bool:
        item_orm = OrderItemORM.from_entity(item_data)
        async with self.database.get_session() as session:
            session.add(item_orm)
        return item_orm

    async def get_order_by_oid_with_items(self, oid: uuid.UUID):
        # Используем joinedload для загрузки связанных элементов
        order_stmt = select(OrderORM).options(joinedload(OrderORM.items)).where(OrderORM.oid == oid).limit(1)

        async with self.database.get_read_only_session() as session:
            order = await session.scalar(order_stmt)

        if order is None:
            return None

        return order

        