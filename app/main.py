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

products = [
    {
        "id": 1,
        "name": "Keyboard",
        "category": "Tech",
        "price": 15,
        "stock": 7,
        "minimum_stock": 2
    },
    {
        "id": 2,
        "name": "Mouse",
        "category": "Tech",
        "price": 5,
        "stock": 11,
        "minimum_stock": 2
    }
]

@app.get("/")
def home_page():
    return {"message": "Smart Inventory API"}

@app.get("/products")
def get_products():
    for product in products:
        product["status"] = get_stock_status(
        product["stock"],
        product["minimum_stock"]
        )
    return products

@app.get("/products/low-stock")
def get_low_stock_products():
    low_stock_products = []

    for product in products:
        if product["stock"] > 0 and product["stock"] <= product["minimum_stock"]:
            low_stock_products.append(product)

    return low_stock_products

@app.get("/products/out-of-stock")
def get_out_of_stock():
    out_of_stock = []

    for product in products:
        if product["stock"] == 0:
            out_of_stock.append(product)
        
    return out_of_stock

@app.get("/products/search")
def search_products(name: str):
    product_name = []

    for product in products:
        if  name.lower() in product["name"].lower():
            product_name.append(product)

    return product_name

@app.get("/products/category")
def filter_by_category(category: str):
    product_category = []

    for product in products:
        if category.lower() == product["category"].lower():
            product_category.append(product)

    return product_category

@app.get("/stats")
def get_stats():
    low_stock_count = 0
    out_of_stock_count = 0
    inventory_value = 0

    for product in products:
        inventory_value += product["price"] * product["stock"]
        
        if product["stock"] == 0:
            out_of_stock_count += 1
        elif product["stock"] > 0 and product["stock"] <= product["minimum_stock"]:
            low_stock_count += 1

    return {
        "total_products": len(products),
        "low_stock": low_stock_count,
        "out_of_stock": out_of_stock_count,
        "inventory_value": inventory_value
    }

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            product["status"] = get_stock_status(
                product["stock"],
                product["minimum_stock"]
            )
            return product
        
    raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

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
def update_product(product_id: int, product_update: ProductUpdate):
    for product in products:
        if product["id"] == product_id:
            update_data = product_update.model_dump(exclude_unset=True)

            product.update(update_data)

            return product
        
    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

@app.delete("/products/{product_id}")
def remove_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": "Product deleted"}

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


def get_stock_status(stock: int, minimum_stock: int) -> str:
    if stock == 0:
        status = "OUT OF STOCK"
    elif stock <= minimum_stock:
        status = "LOW STOCK"
    else:
        status = "IN STOCK"

    return status