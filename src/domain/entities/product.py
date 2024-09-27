from uuid import UUID
from dataclasses import dataclass, field


@dataclass
class Product:
    oid: UUID | None = None
    title: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None
