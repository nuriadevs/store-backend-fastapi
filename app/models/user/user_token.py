from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey

class UserToken(Base):
    """
    Modelo que representa los tokens de acceso y actualización de los usuarios.

    Atributos:
        id (int): Identificador único del token.
        user_id (int): Referencia al ID del usuario al que pertenece el token.
        access_key (str): Clave de acceso asociada al token.
        refresh_key (str): Clave de renovación asociada al token.
        created_at (datetime): Fecha y hora en que se creó el token.
        expires_at (datetime): Fecha y hora en que el token expirará.

    Esta tabla almacena los tokens de acceso y renovación utilizados para autenticar y mantener la sesión del usuario.
    """
    
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('users.id'))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")