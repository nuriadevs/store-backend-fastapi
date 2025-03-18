from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.user.user import User
from app.responses.user import UserDeleteResponse, UserResponse
from app.services.user import delete_user_account, fetch_user_detail
from app.dependencies.admin import is_admin
from app.dependencies.user import get_current_user

admin_user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not Found"}},
)


@admin_user_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def fetch_user_id(
    user_id: int, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
    ):
    """
    Obtiene los detalles de un usuario específico por su ID.

    Este endpoint permite que un administrador autorizado obtenga la información de una cuenta de usuario 
    en función de su ID. 

    Args:
       - user_id: El ID del usuario cuya información se desea obtener.
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias para interactuar con la base de datos.
       - user: El usuario actual que realiza la solicitud, verificado como administrador.
    Returns:
       - UserResponse: Los detalles del usuario solicitado, como su id, username, email si esta activo y fecha de la creación.

    """
    return await fetch_user_detail(user_id, session)



@admin_user_router.delete("/{user_id}",response_model=UserDeleteResponse, status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
):

    """
    Eliminar un usuario específico por su ID.

    Permite a un usuario admin eliminar un usuario específico de la base de datos.

    Args:
       - user_id (int): El ID del usuario a eliminar.
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias.

    Returns:
       - status_code: 204 No Content, indicando que el usuario fue eliminado con éxito.
    """


    return await delete_user_account(user_id, session)


