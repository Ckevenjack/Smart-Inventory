from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    minimum_stock: int= Field(ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    category: Optional[str] = Field(default=None, min_length=2, max_length=50)
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    minimum_stock: Optional[int] = Field(default=None, ge=0)

    @field_validator(
        "name",
        "category",
        "price",
        "stock",
        "minimum_stock")
    def product_validator(cls, value):
        if value is None:
            raise ValueError("Field cannot be null")
            
        return value