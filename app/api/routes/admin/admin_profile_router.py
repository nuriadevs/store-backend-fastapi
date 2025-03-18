
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.user.user import User
from app.responses.user_profile import UserProfileDeleteResponse, UserProfileResponse
from app.services import user_profile
from app.dependencies.admin import is_admin
from app.dependencies.user import get_current_user


admin_profile_router = APIRouter(
    prefix="/users/profile", 
    tags=["User Profile"],
    responses={404: {"description": "Not found"}}
)



@admin_profile_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserProfileResponse)
async def fetch_user_profile_detail(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
    ):
    
    """
    Obtener la información del perfil de un usuario específico por su ID.

    Permite que un administrador autorizado obtenga los detalles del perfil de un usuario 
    en función de su ID.

    Args:
       - user_id: El ID del usuario cuyo perfil se desea obtener.
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias.
       - user (User): El usuario autenticado, que debe ser administrador para acceder a esta información.

    Returns:
       - UserProfileResponse: El perfil del usuario solicitado, que incluye detalles como su nombre, dirección y más.
    """

    return await user_profile.get_user_profile(user_id, session)




@admin_profile_router.delete("/{user_id}",response_model=UserProfileDeleteResponse, status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
):
    """
    Eliminar el perfil de un usuario por su ID.

    Permite que un administrador autorizado elimine el perfil de un usuario. 
    La eliminación es lógica , marca el perfil como eliminado en la base de datos.

    Args:
       - user_id: El ID del usuario cuyo perfil se desea eliminar.
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias.
       - user (User): El usuario autenticado, que debe ser administrador para realizar la operación.

    Returns:
       - status_code: No se devuelve ningún contenido en caso de éxito (204 No Content).
    """
    return await user_profile.delete_user_profile(user_id, session)
