from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.product import Product

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock: int
    minimum_stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    minimum_stock: Optional[int] = None

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Smart Inventory API"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return products

@app.get("/products/low-stock")
def get_low_stock_products(db: Session = Depends(get_db)):

    low_stock_products = (
        db.query(Product)
        .filter(
            Product.stock > 0,
            Product.stock <= Product.minimum_stock
        )
        .all()
    )

    return low_stock_products

@app.get("/products/out-of-stock")
def get_out_of_stock(db: Session = Depends(get_db)):

    out_of_stock = (
        db.query(Product)
        .filter(Product.stock == 0)
        .all()
    )
    
    return out_of_stock

@app.get("/products/search")
def search_products(
    name: str,
    db: Session = Depends(get_db)):

    product_name = (
        db.query(Product)
        .filter(Product.name.ilike(f"%{name}%"))
        .all()
    )

    return product_name

@app.get("/products/category")
def filter_by_category(
    category: str,
    db: Session = Depends(get_db)):

    product_category = (
        db.query(Product)
        .filter(Product.category.ilike(category))
        .all()
    )

    return product_category

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    total_products = db.query(Product).count()

    low_stock = (
        db.query(Product)
        .filter(
            Product.stock > 0,
            Product.stock <= Product.minimum_stock
        )
        .count()
    )

    out_of_stock = (
        db.query(Product)
        .filter(Product.stock == 0)
        .count()
    )

    inventory_value = 0

    products = db.query(Product).all()
    for product in products:
        inventory_value += product.price * product.stock

    return {
        "total_products": total_products,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "inventory_value": inventory_value
    }

@app.get("/products/{product_id}")
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

    return product

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)):

    if products:
        new_id = max(product["id"] for product in products) + 1
    else:
        new_id = 1

    new_product = Product(
        name=product.name,
        category=product.category,
        price=product.price,
        stock=product.stock,
        minimum_stock=product.minimum_stock
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@app.patch("/products/{product_id}")
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)):
        
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    update = product_update.model_dump(exclude_unset=True)

    for field, value in update.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

@app.delete("/products/{product_id}")
def remove_product(
    product_id: int,
    db: Session = Depends(get_db)):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}


def get_stock_status(stock: int, minimum_stock: int) -> str:
    if stock == 0:
        status = "OUT OF STOCK"
    elif stock <= minimum_stock:
        status = "LOW STOCK"
    else:
        status = "IN STOCK"

    return status