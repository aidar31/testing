from uuid import UUID
from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import select

from src.gateways.postgresql.database import Database
from src.gateways.postgresql.models.product import ProductORM

from src.domain.entities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def get_by_oid(self, oid: UUID) -> ProductORM | None:
        pass

    async def get_all(self) -> list[ProductORM] | None:
        pass

    async def create(self, product: Product) -> ProductORM:
        pass

    async def update(self, oid: UUID, product: Product) -> ProductORM:
        pass

    async def delete(self, oid: UUID) -> bool:
        pass


@dataclass
class ORMProductRepository(IProductRepository):
    database: Database

    async def get_by_oid(self, oid: UUID) -> ProductORM | None:
        stmt = select(ProductORM).where(ProductORM.oid == oid).limit(1)
        async with self.database.get_read_only_session() as session:
            return await session.scalar(stmt)

    async def get_all(self) -> list[ProductORM] | None:
        stmt = select(ProductORM)
        async with self.database.get_read_only_session() as session:
            result = await session.scalars(stmt)
            return result.all()

    async def create(self, product: Product) -> ProductORM:
        product_orm = ProductORM.from_entity(product)
        async with self.database.get_session() as session:
            session.add(product_orm)
        return product_orm

    async def update(self, oid: UUID, product: Product) -> ProductORM:
        async with self.database.get_session() as session:
            stmt = select(ProductORM).where(ProductORM.oid == oid)
            product_orm: ProductORM = await session.scalar(stmt)
            if product_orm:
                product_orm.title = product.title
                product_orm.description = product.description
                product_orm.price = product.price
                product_orm.quantity = product.quantity
                return product_orm
            return None

    async def delete(self, oid: UUID) -> bool:
        async with self.database.get_session() as session:
            stmt = select(ProductORM).where(ProductORM.oid == oid)
            product_orm = await session.scalar(stmt)
            if product_orm:
                await session.delete(product_orm)
                return True
            return False
