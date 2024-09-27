import uuid
from pydantic import BaseModel


class GetProductResponseSchema(BaseModel):
    title: str
    description: str
    price: float
    quantity: int

class UpdateProductRequestSchema(GetProductResponseSchema):
    pass

class CreateProductRequestSchema(GetProductResponseSchema):
    pass


class DeleteProductResponseSchema(BaseModel):
    status: bool