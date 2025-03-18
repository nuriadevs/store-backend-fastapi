from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.user.user import User
from app.models.user.user_profile import UserProfile
from app.responses.user_profile import UserProfileResponse
from app.schemas.user_profile import UserProfileRequest, UserProfileUpdateAdressRequest
from app.services.user_profile import create_user_profile, get_user_profile, update_user_address, update_user_profile
from app.dependencies.user import get_current_user


profile_router = APIRouter(
    prefix="/users/profile", 
    tags=["User Profile"],
    responses={404: {"description": "Not found"}}
)


@profile_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_profile(data: UserProfileRequest, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)
):
    
    """
    Crear el perfil de un usuario.

    Permite que un usuario cree o registre su perfil proporcionando la información necesaria.

    Args:
        - data: Los datos del perfil del usuario que se desean crear.
        - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias.
        - current_user (User): El usuario actualmente autenticado que está realizando la operación.

    Returns:
        UserProfileResponse: El perfil del usuario recién creado.
    """    
    return await create_user_profile(data, session, current_user)



@profile_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserProfileResponse)
async def fetch_user_profile( 
    session: Session = Depends(get_session),
    current_user: UserProfile = Depends(get_current_user)):
    """
    Permite que un usuario autenticado obtenga su propia información de cuenta.

    Args:
       - user (User): El usuario autenticado. Se obtiene mediante la inyección de dependencias usando el `Depends(get_current_user)`.

    Returns:
       - UserResponse: Los detalles del usuario autenticado, como el id, username, email, si esta activado y fecha de creación.
    """
    return await get_user_profile(current_user.id, session)



@profile_router.put("/update", status_code=status.HTTP_200_OK)
async def update_profile(data: UserProfileRequest, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)
): 
    """
    Actualizar el perfil de un usuario.

    Permite que un usuario autenticado actualice su perfil con nuevos datos.

    Args:
       - data: Los nuevos datos del perfil del usuario que se desean actualizar.
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias.
       - current_user (User): El usuario actualmente autenticado que está realizando la operación.

    Returns:
        UserProfileResponse: El perfil del usuario actualizado.
    """
    return await update_user_profile(data, session, current_user)


@profile_router.patch("/{user_id}/address", status_code=status.HTTP_200_OK)
async def update_user_profile_address(
    data: UserProfileUpdateAdressRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar la dirección de un usuario.

    Permite que un usuario autenticado actualice su dirección en su perfil.

    Args:
       - data: Los datos de la dirección que se desean actualizar.
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias.
       - current_user (User): El usuario actualmente autenticado que está realizando la operación.

    Returns:
        UserProfileResponse: El perfil del usuario con la dirección actualizada.
    """
    return await update_user_address(data, session, current_user)




