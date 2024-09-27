import uuid
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from src.core.containers import container

from src.gateways.postgresql.models.order import OrderItemORM
from src.gateways.postgresql.models.order_item import OrderItemORM
from src.gateways.postgresql.repositories.order import IOrderRepository

from src.rest.orders.schemas import GetOrderResponseSchema, CreateOrderRequestSchema

router = APIRouter(tags=["Orders"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    description="Создание Заказа",
    responses={
        status.HTTP_200_OK: {"model": GetOrderResponseSchema}
    }
)
async def create_order_handler(
    order_data: CreateOrderRequestSchema
) -> GetOrderResponseSchema: 
    pass