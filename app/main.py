from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app import models
from app.database import Base, engine

from app.routers.products import router as product_router
from app.routers.users import router as user_router
from app.routers.customers import router as customer_router
from app.routers.categories import router as category_router
from app.routers.suppliers import router as supplier_router
from app.routers.sales import router as sale_router
from app.routers.sale_items import router as sale_item_router
from app.routers.payments import router as payment_router
from app.routers.receipts import router as receipt_router
from app.routers.auth import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="pos Api")

app.include_router(product_router)
app.include_router(user_router)
app.include_router(customer_router)
app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(sale_router)
app.include_router(sale_item_router)
app.include_router(payment_router)
app.include_router(receipt_router)
app.include_router(auth_router)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": (
                "Database constraint violated: a value is duplicated, a related "
                "record does not exist, or the record is still in use"
            )
        },
    )


@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "POS System Backend API is active",
    }
