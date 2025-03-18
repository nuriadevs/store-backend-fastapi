from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy import Boolean, Column, Integer, String, func
from sqlalchemy.orm import mapped_column,relationship
from app.models.user.user_roles_association import user_roles_association
from app.models.user.user_token import UserToken

class User(Base):
    """
    Modelo que representa a un usuario en el sistema.

    Atributos:
        id (int): Identificador único del usuario.
        username (str): Nombre de usuario único.
        email (str): Correo electrónico único del usuario.
        password (str): Contraseña del usuario.
        deleted_at (datetime): Fecha y hora de eliminación lógica del usuario.
        verified_at (datetime): Fecha y hora de verificación del usuario.
        is_active (bool): Estado de activación de la cuenta del usuario.
        created_at (datetime): Fecha y hora de creación del usuario.
        updated_at (datetime): Fecha y hora de la última actualización del usuario.

    Relaciones:
        tokens (UserToken): Relación con los tokens de acceso y actualización del usuario.
        roles (UserRole): Relación con los roles asignados al usuario.
        profile (UserProfile): Relación con el perfil del usuario.

    Métodos:
        get_context_string(context: str): Genera una cadena de contexto utilizada para validación y autenticación.
    """
    
    __tablename__ = 'users'  

    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String(100),nullable=False) 
    email = Column(String(100), unique=True, nullable=False) 
    password = Column(Text, nullable=False) 
    deleted_at = Column(TIMESTAMP, nullable=True)  
    verified_at = Column(TIMESTAMP, nullable=True)  
    is_active = Column(Boolean, default=False, nullable=False)  
    created_at = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)  
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)  

    tokens = relationship("UserToken", back_populates="user") 
    roles = relationship("UserRole", secondary=user_roles_association, backref="users")

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def get_context_string(self, context: str):
        password_suffix = self.password[-6:] if self.password and len(self.password) >= 6 else "000000"
        updated_at_str = self.updated_at.strftime('%m%d%Y%H%M%S') if self.updated_at else "00000000000000"
    
        return f"{context}{password_suffix}{updated_at_str}".strip()

