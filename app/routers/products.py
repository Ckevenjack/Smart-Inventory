from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductUpdate

from app.database import get_db
from app.models.product import Product

from app.services import product_service 

router = APIRouter()

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return product_service.get_products(db)

@router.get("/products/low-stock")
def get_low_stock_products(db: Session = Depends(get_db)):
    return product_service.get_low_stock_products(db)

@router.get("/products/out-of-stock")
def get_out_of_stock(db: Session = Depends(get_db)):
    return product_service.get_out_of_stock(db)

@router.get("/products/search")
def search_products(
    name: str,
    db: Session = Depends(get_db)):
    return product_service.search_products(db, name)

@router.get("/products/category")
def filter_by_category(
    category: str,
    db: Session = Depends(get_db)):

    return product_service.filter_by_category(db, category)

@router.get("/products/{product_id}")
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)):

    product = product_service.get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

    return product

@router.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)):

    new_product = product_service.create_product(db, product)

    return new_product

@router.patch("/products/{product_id}")
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)):
        
    product = product_service.update_product(db, product_id, product_update)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@router.delete("/products/{product_id}")
def remove_product(
    product_id: int,
    db: Session = Depends(get_db)):

    product = product_service.remove_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product
