from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import  Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func



class Category(Base):
    """
    Representa una categoría de productos.

    Atributos:
        id (int): Identificador único de la categoría.
        name (str): Nombre de la categoría (único).
        description (str): Descripción de la categoría.
        deleted_at (datetime, opcional): Fecha de eliminación lógica.
        created_at (datetime): Fecha de creación.
        updated_at (datetime): Fecha de última actualización.

    Relación:
        products (list[Product]): Productos asociados a esta categoría.
    """
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    deleted_at = Column(TIMESTAMP, nullable=True)  
    created_at = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)  
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)  
    
    products = relationship("Product", back_populates="category", lazy="joined")
