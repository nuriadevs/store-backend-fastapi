from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, TIMESTAMP


class OrderItem(Base):
    """
    Representa un artículo en un pedido.

    Atributos:
        id (int): Identificador único del artículo del pedido.
        order_id (int): ID del pedido al que pertenece.
        product_id (int): ID del producto en el artículo.
        quantity (int): Cantidad de productos en el artículo.
        subtotal (Decimal): Subtotal por el artículo (precio * cantidad).
        deleted_at (datetime, opcional): Fecha de eliminación lógica.

    Relaciones:
        order (Order): Pedido al que pertenece este artículo.
        product (Product): Producto asociado a este artículo.
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)  

    order = relationship("Order", back_populates="order_items", lazy="joined")
    product = relationship("Product", back_populates="order_items", lazy="joined")
    
