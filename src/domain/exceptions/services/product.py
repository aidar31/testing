from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ProductNotFound(ApplicationException):
    """Product с таким oid не найден."""

    @property
    def message(self):
        return "Product not found."


@dataclass(eq=False)
class ProductNotDeleted(ApplicationException):
    """ Удаление продукта не удалось """

    @property
    def message(self):
        return "Product not deleted."
