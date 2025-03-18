from sqlalchemy import Table, Column, ForeignKey, Integer
from app.core.database import Base
from app.models.user.user_roles import UserRole 

"""
    Asociación entre usuarios y roles, utilizada para mapear la relación muchos a muchos.
    
    Atributos:
        user_id (int): ID del usuario que se asocia al rol.
        role_id (int): ID del rol asignado al usuario.

    Esta tabla no tiene un modelo en sí misma, ya que solo maneja la relación entre los usuarios y sus roles.
"""
user_roles_association = Table(

    
    
    "user_roles_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("user_roles.id"))
)


