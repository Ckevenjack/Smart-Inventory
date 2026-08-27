from sqlalchemy import text
from app.database import engine
from app.models.product import Product
from app.database import SessionLocal

#with engine.connect() as connection:
#    result = connection.execute(text("SELECT 1"))
    #print(result.scalar())
    
    # Check table
    #print(Product.__tablename__)

db = SessionLocal()

# check product 
# products = db.query(Product).all()

# for product in products:
#     print(product.name)

# db.close()

new_product = Product(
    name="Monitor",
    category="Tech",
    price=120,
    stock=5,
    minimum_stock=2
)

db.add(new_product)
db.commit()
db.refresh(new_product)

print(new_product.id)
print(new_product.name)
db.close()