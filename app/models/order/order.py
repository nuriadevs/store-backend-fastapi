from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql import func


class Order(Base):
    """
    Representa una orden de compra realizada por un usuario.

    Atributos:
        id (int): Identificador único de la orden.
        user_id (int): ID del usuario que realizó la orden.
        total_price (Decimal): Precio total de la orden.
        status (str): Estado actual de la orden (por ejemplo, 'pendiente').
        deleted_at (datetime, opcional): Fecha de eliminación lógica.
        created_at (datetime): Fecha de creación de la orden.
        updated_at (datetime): Fecha de última actualización de la orden.

    Relaciones:
        order_items (OrderItem): Artículos asociados con esta orden.
    """
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(50), nullable=False, default="pendiente")
    deleted_at = Column(TIMESTAMP, nullable=True)  
    created_at = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)  
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)  
    
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="joined")