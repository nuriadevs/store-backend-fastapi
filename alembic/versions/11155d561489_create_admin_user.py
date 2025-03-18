from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone
from app.core.settings import get_settings  
from app.core.security import hash_password

settings = get_settings()



# revision identifiers, used by Alembic.
revision: str = '11155d561489'
down_revision: Union[str, None] = 'bccd3ca66f01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Tablas necesarias
user_table = sa.table(
    "users",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String),
    sa.Column("email", sa.String),
    sa.Column("password", sa.String),
    sa.Column("is_active", sa.Boolean),
    sa.Column("deleted_at", sa.DateTime),
    sa.Column("verified_at", sa.DateTime),
    sa.Column("updated_at", sa.DateTime),
    sa.Column("created_at", sa.DateTime),  
)

role_table = sa.table(
    "user_roles",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
)

user_roles_association = sa.table(
    "user_roles_association",
    sa.Column("user_id", sa.Integer),
    sa.Column("role_id", sa.Integer),
)


def upgrade():
    # Insertar el rol "admin" si no existe
    op.bulk_insert(
        role_table,
        [
            {
                "id": 1,  # ID para el rol admin
                "name": "admin",
            }
        ],
    )

    # Insertar el usuario admin
    user_id = 1  
    now = datetime.now(timezone.utc)  # Obtener la fecha y hora actual
    op.bulk_insert(
        user_table,
        [
            {
                "id": user_id,
                "username": "Admin",
                "email": "admin@evoltronic.com", 
                "password": hash_password(settings.ADMIN_PASSWORD),  
                "is_active": True,
                "deleted_at": None,
                "verified_at": now,
                "updated_at": now,
                "created_at": now,  
            }
        ],
    )

    # Asignar el rol "admin" al usuario creado
    op.bulk_insert(
        user_roles_association,
        [
            {
                "user_id": user_id,
                "role_id": 1, 
            }
        ],
    )

def downgrade():
    # Eliminar el usuario admin
    op.execute(
        user_table.delete().where(user_table.c.email == "admin@evoltronic.com")
    )

    # Eliminar el rol "admin"
    op.execute(
        role_table.delete().where(role_table.c.name == "admin")
    )