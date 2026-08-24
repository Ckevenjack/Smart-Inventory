from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

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
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
        
    raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    if products:
        new_id = max(product["id"] for product in produts) + 1
    else:
        new_id = 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "category": product.category,
        "price": product.price,
        "stock": product.stock,
        "minimum_stock": product.minimum_stock
    }
    products.append(new_product)

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