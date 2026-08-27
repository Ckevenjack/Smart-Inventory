from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    stock: Mapped[int] = mapped_column()
    minimum_stock: Mapped[int] = mapped_column()
