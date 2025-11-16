from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import String, Float, Integer, ForeignKey, Boolean, DateTime, text, func 
from datetime import datetime  
class Category(db.Model):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category"
    )

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    category_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    # --- ДОДАНО (Частина 4) ---
    # Ми використовуємо server_default, щоб уникнути помилки NOT NULL
    # Для SQLite 'True' - це '1'
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text('1'))

    # --- ДОДАНО (Частина 6) ---
    # Використовуємо server_default=func.now()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    # --- Кінець доданого блоку ---

    def __repr__(self):
        return f'<Product {self.name}>'