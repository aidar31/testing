from fastapi import FastAPI

from src.rest.products.handlers import router as product_router
from src.rest.orders.handlers import router as order_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Storage Api's",
        docs_url="/api/docs",
        description="Тестовое задание",
        debug=True,
    )

    app.include_router(product_router, prefix="/products")
    app.include_router(order_router, prefix="/orders")

    return app
