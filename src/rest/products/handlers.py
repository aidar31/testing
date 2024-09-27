import uuid
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from src.core.containers import container

from src.domain.entities.product import Product

from src.domain.services.product import IProductService

from src.domain.exceptions.services.product import ProductNotFound
from src.domain.exceptions.base import ApplicationException

from src.rest.schemas import ErrorSchema
from src.rest.products.schemas import (
    GetProductResponseSchema,
    CreateProductRequestSchema,
    UpdateProductRequestSchema
)


router = APIRouter(tags=["Products"])


@router.get(
    "/{oid}",
    status_code=status.HTTP_200_OK,
    description="Возращает Product по id",
    responses={
        status.HTTP_200_OK: {"model": GetProductResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def get_product_by_oid(
    oid: uuid.UUID,
) -> GetProductResponseSchema:
    try:
        service = await container.get(IProductService)
        product = await service.get_product(oid)

    except ProductNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": exception.message}
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return product


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Создает Product",
    responses={
        status.HTTP_201_CREATED: {"model": GetProductResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def create_product_handler(
    product: CreateProductRequestSchema,
) -> GetProductResponseSchema:
    try:
        service = await container.get(IProductService)
        product_result = await service.create_product(
            Product(
                title=product.title,
                description=product.description,
                price=product.price,
                quantity=product.quantity,
            )
        )
    except ProductNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": exception.message}
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return product


@router.put(
    "/{oid}",
    status_code=status.HTTP_200_OK,
    description="Update PUT Method product",
    responses={
        status.HTTP_200_OK: {"model": GetProductResponseSchema}
    }
)
async def product_product_handler(
    oid: uuid.UUID,
    product_data: UpdateProductRequestSchema
) -> GetProductResponseSchema:
    try:
        service = await container.get(IProductService)
        result_product = await service.update_product(
            oid, product_data
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return result_product

@router.delete(
    "/{oid}",
    status_code=status.HTTP_200_OK,
    description="Delete product by id",
)
async def delete_product_handler(
    oid: uuid.UUID 
):
    try:
        service = await container.get(IProductService)
        result = await service.delete_product(oid)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    return result