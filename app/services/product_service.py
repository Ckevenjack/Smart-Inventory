from sqlalchemy.orm import Session

from app.models.product import Product

from app.schemas.product import ProductCreate, ProductUpdate

def get_products(db: Session):
    products = db.query(Product).all()

    return products

def get_product_by_id(
    db: Session,
    product_id: int):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    return product

def create_product(
    db: Session,
    product: ProductCreate):

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
    db:Session,
    product_id: int,
    product_update: ProductUpdate):
        
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        return None

    update = product_update.model_dump(exclude_unset=True)

    for field, value in update.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

def remove_product(
    db: Session,
    product_id: int):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        return None

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}

def get_low_stock_products(db: Session):

    low_stock_products = (
        db.query(Product)
        .filter(
            Product.stock > 0,
            Product.stock <= Product.minimum_stock
        )
        .all()
    )

    return low_stock_products

def get_out_of_stock(db: Session):

    out_of_stock = (
        db.query(Product)
        .filter(Product.stock == 0)
        .all()
    )
    
    return out_of_stock

def search_products(
    db: Session,
    name: str):

    product_name = (
        db.query(Product)
        .filter(Product.name.ilike(f"%{name}%"))
        .all()
    )

    return product_name

def filter_by_category(
    db: Session,
    category: str):

    product_category = (
        db.query(Product)
        .filter(Product.category.ilike(category))
        .all()
    )

    return product_category