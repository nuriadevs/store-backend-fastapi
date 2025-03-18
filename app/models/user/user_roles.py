from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserRole(Base):
    """
    Modelo que representa los roles de los usuarios en el sistema.

    Atributos:
        id (int): Identificador único del rol.
        name (str): Nombre del rol, debe ser único.

    Esta tabla define los roles que un usuario puede tener, como 'admin', 'usuario', etc.
    """
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  
