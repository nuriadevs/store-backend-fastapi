from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func


class Product(Base):

    """
    Representa un producto disponible para la venta en la tienda.

    Atributos:
        id (int): Identificador único del producto.
        name (str): Nombre del producto.
        description (str, opcional): Descripción detallada del producto.
        price (Decimal): Precio del producto.
        stock (int): Cantidad de unidades disponibles en inventario.
        category_id (int, opcional): ID de la categoría a la que pertenece el producto.
        deleted_at (datetime, opcional): Fecha de eliminación lógica.
        created_at (datetime): Fecha de creación del producto.
        updated_at (datetime): Fecha de última actualización del producto.

    Relaciones:
        category (Category): Categoría a la que pertenece el producto.
        order_items (OrderItem): Artículos de pedido asociados con este producto.
    """
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)  
    created_at = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)  
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)  
    

    category = relationship("Category", back_populates="products", lazy="joined")
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan", lazy="joined")
    