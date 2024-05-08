from fastapi import FastAPI, HTTPException, Depends, status
from pydantic_models import ProductsBase
from typing import Annotated
import models
from database import engine, SessionLocal, db_dependency
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import auth
from auth import get_active_user
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_dependency = Annotated[dict, Depends(get_active_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed!")
    return {"user": user}


@app.post("/products", status_code=status.HTTP_201_CREATED)
async def add_product(
    user: user_dependency, db: db_dependency, create_product: ProductsBase
):
    try:
        add_product = models.Products(
            name=create_product.name,
            price=create_product.price,
            cost=create_product.cost,
            img_url=create_product.img_url,
            stock_quantity=create_product.stock_quantity,
            user_id=user.get("id"),
        )
        db.add(add_product)
        db.commit()
        db.refresh(add_product)
        return {"message": "Product added successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
