from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.user.user import User
from app.responses.user import UserResponse, UsernameUpdateRequest
from app.schemas.user import  RegisterUserRequest, VerifyUserRequest
from app.services.user import activate_user_account, create_user_account, fetch_user_detail, update_user_account
from app.dependencies.admin import is_admin
from app.dependencies.user import get_current_user

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not Found"}},
)

@user_router.post("", status_code= status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data:RegisterUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    Registra un nuevo usuario en la base de datos.

    Args:
       - data (RegisterUserRequest): Datos del usuario a registrar (nombre, email, contraseña, etc.).
       - background_tasks (BackgroundTasks): Permite ejecutar tareas en segundo plano, como enviar un email de confirmación.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.
    Returns:
       - UserResponse: Respuesta con los datos del usuario registrado.
    """
    
    return await create_user_account(data, session, background_tasks) 

@user_router.post("/verify", status_code= status.HTTP_200_OK)
async def verify_user_account(data:VerifyUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    Verifica la cuenta de un usuario utilizando sus datos proporcionados.
    El proceso de verificación envia un token de verificación por email.

    Args:
       - data (VerifyUserRequest): Datos necesarios para verificar la cuenta del usuario. 
       - (BackgroundTasks): Tareas en segundo plano para realizar procesos adicionales, como enviar un email.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
      - Mensaje que confirma que la cuenta del usuario ha sido verificada y activada exitosamente.
    """
    return await activate_user_account(data, session, background_tasks) 

@user_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def fetch_user(user: User = Depends(get_current_user)):
    """
    Permite que un usuario autenticado obtenga su propia información de cuenta.

    Args:
       - user (User): El usuario autenticado. Se obtiene mediante la inyección de dependencias usando el `Depends(get_current_user)`.

    Returns:
       - UserResponse: Los detalles del usuario autenticado, como el id, username, email, si esta activado y fecha de creación.
    """
    return user

@user_router.put("/{user_id}", response_model=UsernameUpdateRequest,status_code=status.HTTP_200_OK)
async def update_user(
    data: UsernameUpdateRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    """ 
    Actualiza el username de usuario de un usuario específico.

    Un administrador o al propio usuario actualizar su nombre de usuario.

    Args:
    - user_id (int): El ID del usuario cuya información se desea actualizar. 
    - data (UsernameUpdateRequest): Los datos necesarios para actualizar el nombre de usuario del usuario. 
    - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias. 
    - current_user (User): El usuario actual realizando la solicitud. 
    - user (User): El usuario actual, que debe tener permisos de administrador.

    Returns: 
        - UsernameUpdateRequest: El usename de usuario actualizado. 
    """    
    return await update_user_account(data, session, current_user)

