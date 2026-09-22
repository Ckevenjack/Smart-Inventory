from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_products(db: Session):
    stmt = select(Product)
    products = db.scalars(stmt).all()

    return products


def get_product_by_id(db: Session, product_id: int):
    stmt = (
        select(Product)
        .where(Product.id == product_id)
    )

    product = db.scalars(stmt).first()

    return product


def create_product(db: Session, product: ProductCreate):
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


def update_product(
    db: Session,
    product_id: int,
    product_update: ProductUpdate
):
    stmt = (
        select(Product)
        .where(Product.id == product_id)
    )

    product = db.scalars(stmt).first()

    if product is None:
        return None

    update = product_update.model_dump(
        exclude_unset=True
    )

    for field, value in update.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


def remove_product(db: Session, product_id: int):
    stmt = (
        select(Product)
        .where(Product.id == product_id)
    )

    product = db.scalars(stmt).first()

    if product is None:
        return None

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}


def get_low_stock_products(db: Session):
    stmt = (
        select(Product)
        .where(
            Product.stock > 0,
            Product.stock <= Product.minimum_stock
        )
    )

    low_stock_products = db.scalars(stmt).all()

    return low_stock_products


def get_out_of_stock(db: Session):
    stmt = (
        select(Product)
        .where(Product.stock == 0)
    )

    out_of_stock = db.scalars(stmt).all()

    return out_of_stock


def search_products(db: Session, name: str):
    stmt = (
        select(Product)
        .where(Product.name.ilike(f"%{name}%"))
    )

    products = db.scalars(stmt).all()

    return products


def filter_by_category(db: Session, category: str):
    stmt = (
        select(Product)
        .where(Product.category.ilike(category))
    )

    products = db.scalars(stmt).all()

    return products