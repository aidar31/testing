import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi.requests import Request

from src.domain.entities.product import Product
from src.domain.exceptions.services.product import ProductNotFound, ProductNotDeleted

from src.gateways.postgresql.repositories.product import IProductRepository
from src.gateways.postgresql.models.product import ProductORM


class IProductService(ABC):
    @abstractmethod
    async def get_product(self, product_id: uuid.UUID) -> Product | None:
        pass

    @abstractmethod
    async def create_product(self, product_data: Product) -> Product:
        pass

    @abstractmethod
    async def update_product(
        self, product_id: uuid.UUID, product_data: Product
    ) -> Product | None:
        pass

    @abstractmethod
    async def delete_product(
        self, product_id: uuid.UUID
    ) -> bool:
        pass

@dataclass
class ProductService(IProductService):
    repository: IProductRepository

    async def get_product(self, product_id: uuid.UUID) -> Product | None:
        product = await self.repository.get_by_oid(product_id)
        if not product:
            raise ProductNotFound()
        return product

    async def create_product(self, product_data: Product) -> Product:
        product = await self.repository.create(product_data)
        return product

    async def update_product(
        self, product_id: uuid.UUID, product_data: Product
    ) -> Product | None:
        product = await self.repository.update(product_id, product_data)
        if not product:
            raise ProductNotFound()
        return product

    async def delete_product(
        self, product_id: uuid.UUID
    ) -> bool:
        result = await self.repository.delete(product_id)
        return result
