from dishka import provide, Provider, Scope, make_async_container

from src.gateways.postgresql.database import Database
from src.gateways.postgresql.repositories.product import (
    ORMProductRepository,
    IProductRepository,
)
from src.gateways.postgresql.repositories.order import (
    ORMOrderRepository,
    IOrderRepository
)

from src.domain.services.product import IProductService, ProductService
from src.domain.services.order import IOrderService, OrderService

from src.core.configs import settings


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_database(self) -> Database:
        return Database(
            url=settings.POSTGRES_DB_URL,
            ro_url=settings.POSTGRES_DB_URL,
        )

    @provide(scope=Scope.APP)
    async def get_product_repository(self, db: Database) -> IProductRepository:
        return ORMProductRepository(db)

    @provide(scope=Scope.APP)
    async def get_order_repository(self, db: Database) -> IOrderRepository:
        return ORMOrderRepository(db)


    @provide(scope=Scope.APP)
    async def get_order_service(
        self,
        repository: IOrderRepository 
    ) -> IOrderService:
        return OrderService(repository)

    @provide(scope=Scope.APP)
    async def get_product_service(
        self,
        repository: IProductRepository,
    ) -> IProductService:
        return ProductService(repository)


provider = AppProvider()
container = make_async_container(provider)
