from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, mapped_column
from app.core.database import Base


class UserProfile(Base):
    """
    Representa el perfil de usuario con información adicional asociada al usuario.

    Atributos:
        id (int): Identificador único del perfil de usuario.
        user_id (int): ID del usuario asociado al perfil.
        first_name (str): Primer nombre del usuario.
        last_name (str): Apellido del usuario.
        dni (str, opcional): Número de documento de identidad del usuario.
        phone (int, opcional): Número de teléfono del usuario.
        address (str, opcional): Dirección del usuario.
        birth_date (date, opcional): Fecha de nacimiento del usuario.
        city (str, opcional): Ciudad del usuario.
        zip_code (int, opcional): Código postal del usuario.
        created_at (datetime): Fecha de creación del perfil.
        updated_at (datetime): Fecha de última actualización del perfil.
        deleted_at (datetime, opcional): Fecha de eliminación lógica del perfil.

    Relaciones:
        user (User): El usuario asociado a este perfil.
    """
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    dni = Column(String(9), unique=True, nullable=True)
    phone = Column(Integer, nullable=True)
    address = Column(String(150), nullable=True)
    birth_date = Column(Date, nullable=True)
    city = Column(String(80), nullable=True)
    zip_code = Column(Integer, nullable=True)

    user = relationship("User", back_populates="profile")

    created_at = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    
