from sqlalchemy.orm import Session

from app.models.product import Product

def get_stats(db: Session):

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