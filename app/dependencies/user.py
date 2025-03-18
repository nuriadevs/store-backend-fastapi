from fastapi import HTTPException, Security, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.core.security import decode_jwt  
from app.core.database import get_session  
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import joinedload


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Security(oauth2_scheme), session: Session = Depends(get_session)):
    """
    Obtiene al usuario a partir del token JWT.

    Args:
        - token: El token JWT recibido en la solicitud.
        - session: La sesión de la base de datos proporcionada por la dependencia.

    Returns:
        - user: El usuario autenticado.

    Raises:
        - HTTPException: Si el token es inválido o el usuario no existe en la base de datos.
    """
    try:
        payload = decode_jwt(token)

        user_id = payload.get("sub")  
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido: Falta el ID de usuario.")

        try:
            user_id = int(user_id)
        except ValueError:

            raise HTTPException(status_code=401, detail="Formato de ID de usuario inválido.")


        user = session.query(User).options(joinedload(User.roles)).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado.")

        return user

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido o error al recuperar el usuario.")
    finally:
        session.close()
