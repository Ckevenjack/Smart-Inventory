from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.product import Product


def get_stats(db: Session):
    # Total number of products
    total_products = db.scalar(
        select(func.count()).select_from(Product)
    )

    # Number of low-stock products
    low_stock = db.scalar(
        select(func.count())
        .select_from(Product)
        .where(
            Product.stock > 0,
            Product.stock <= Product.minimum_stock
        )
    )

    # Number of out-of-stock products
    out_of_stock = db.scalar(
        select(func.count())
        .select_from(Product)
        .where(Product.stock == 0)
    )

    # Total inventory value
    inventory_value = db.scalar(
        select(
            func.coalesce(
                func.sum(Product.price * Product.stock),
                0
            )
        )
    )

    return {
        "total_products": total_products,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "inventory_value": inventory_value
    }