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