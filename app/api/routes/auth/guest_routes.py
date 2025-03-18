from fastapi import APIRouter, Depends, Header, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.services import user
from app.core.database import get_session
from app.schemas.user import  EmailRequest, ResetRequest
from app.responses.user import LoginResponse


guest_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Iniciar sesión de usuario.

    Permite que un usuario inicie sesión con su nombre de usuario y contraseña, 
    y reciba un token de acceso para realizar futuras solicitudes autenticadas.

    Args:
       - data (OAuth2PasswordRequestForm): Datos de inicio de sesión (usuario y contraseña).
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias.

    Returns:
        LoginResponse: Contiene el token de acceso generado para el usuario.
    """
    
    return await user.get_login_token(data, session)

@guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_token(refresh_token=Header(), session: Session = Depends(get_session)):
    """
    Refrescar el token de autenticación.

    Permite a un usuario obtener un nuevo token de acceso utilizando un refresh token.

    Args:
       - refresh_token (str): El token de refresco proporcionado en los encabezados de la solicitud.
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias.

    Returns:
       - LoginResponse: Contiene el nuevo token de acceso generado para el usuario.
    """
    
    return await user.get_refresh_token(refresh_token, session)

@guest_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(data: EmailRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    Solicitar un enlace de restablecimiento de contraseña.

    Permite a un usuario solicitar un enlace para restablecer su contraseña. 
    Un correo electrónico será enviado con el enlace.

    Args:
       - data (EmailRequest): El correo electrónico del usuario que solicita el restablecimiento de la contraseña.
       - background_tasks (BackgroundTasks): Tareas en segundo plano para enviar el correo electrónico.
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias.

    Returns:
       - JSONResponse: Mensaje de confirmación indicando que el enlace de restablecimiento ha sido enviado.
    """
    
    await user.email_forgot_password_link(data, background_tasks, session)
    return JSONResponse({"message": "Se ha enviado un correo electrónico con un enlace para restablecer la contraseña."})

@guest_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetRequest, session: Session = Depends(get_session)):
    """
    Restablece la contraseña de un usuario.

    Permite a un usuario actualizar su contraseña proporcionando los datos necesarios para la verificación.

    Args:
      - data: Los datos necesarios para realizar el restablecimiento de la contraseña, token y la nueva contraseña.
       - session (Session): La sesión de base de datos proporcionada por la inyección de dependencias para interactuar con la base de datos.

    Returns:
        JSONResponse: Mensaje de éxito confirmando que la contraseña ha sido actualizada.

    """
    await user.reset_user_password(data, session)
    return JSONResponse({"message": "Tu contraseña ha sido actualizada."})