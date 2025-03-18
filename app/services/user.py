from datetime import datetime, timedelta, timezone
from http.client import HTTPException
from fastapi import HTTPException
import logging

from fastapi.responses import JSONResponse
from app.core.exceptions import  DatabaseErrorException, RoleNotFoundException, UnexpectedErrorException, UserEmailExistsException, UserNotFoundException, UserPasswordNotStrong
from app.core.security import decode_jwt,generate_token, hash_password, is_password_strong_enough, load_user, str_decode, str_encode, verify_password
from app.models.user import user_roles_association
from app.models.user.user import User, UserToken
from app.models.user.user_profile import UserProfile
from app.models.user.user_roles import UserRole
from app.models.user.user_token import UserToken
from app.core.settings import get_settings
from app.services.email import send_account_activation_confirmation_email, send_account_verification_email, send_password_reset_email
from app.utils.email_context import FORGOT_PASSWORD, USER_VERIFY_ACCOUNT
from app.utils.string import unique_string
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

settings = get_settings()

async def create_user_account(data, session, background_tasks):
    
    """
    Crea una nueva cuenta de usuario, valida los datos, 
    guarda en la base de datos y envía un correo de verificación.

    Args:
        - data (UserAccountCreateRequest): Datos necesarios para crear la cuenta de usuario.
        - session (Session): Sesión de base de datos.
        - background_tasks (BackgroundTasks): Utilizado para enviar el correo de verificación en segundo plano.

    Returns:
        - User: El objeto de usuario creado.

    Raises:
        - UserEmailExistsException: Si el correo electrónico ya está asociado a una cuenta existente.
        - UserPasswordNotStrong: Si la contraseña proporcionada no cumple con los requisitos de seguridad.
        - RoleNotFoundException: Si no se encuentra el rol "cliente" en la base de datos.
        - HTTPException: Si ocurre un error relacionado con la solicitud HTTP.
        - Exception: Si ocurre un error inesperado durante la creación de la cuenta.
    """

    try:
        user_exist = session.query(User).filter(User.email == data.email).first()
        
        if user_exist:
            raise UserEmailExistsException()
        
        if not is_password_strong_enough(data.password):
            raise UserPasswordNotStrong()
        
        user = User(
            username = data.username,  
            email=data.email,  
            password=hash_password(data.password),  
            is_active=data.is_active if hasattr(data, 'is_active') else False,  
            deleted_at=data.deleted_at if hasattr(data, 'deleted_at') else None,  
            verified_at=data.verified_at if hasattr(data, 'verified_at') else None,  
            updated_at = datetime.now(timezone.utc)
        )

        session.add(user)
        session.commit()
        session.refresh(user)
        

        client_role = session.query(UserRole).filter(UserRole.name == "cliente").first()
        
        if client_role:
            session.execute(user_roles_association.insert().values(user_id=user.id, role_id=client_role.id))
            session.commit()
        else:
            RoleNotFoundException()
        
        
        await send_account_verification_email(user, background_tasks=background_tasks)
            
        return user
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,  
            content={"detail": str(e)} 
        )
 
 
 

async def activate_user_account(data, session, background_tasks):

    """
    Activa la cuenta de usuario tras verificar el token de confirmación.

    Args:
        - data (UserAccountActivationRequest): Contiene el correo electrónico y el token de activación del usuario.
        - session (Session): Sesión de base de datos.
        - background_tasks (BackgroundTasks): Utilizado para enviar un correo de confirmación de activación en segundo plano.

    Returns:
        - User: El objeto de usuario con la cuenta activada.

    Raises:
        - HTTPException 400: Si el token de activación no es válido o ha expirado.
        - HTTPException: Si ocurre un error relacionado con la solicitud HTTP.
        - Exception: Si ocurre un error inesperado durante la creación de la cuenta.
    """

    try:
        user = session.query(User).filter(User.email == data.email).first()
        
        if not user:
            raise HTTPException(status_code=400, detail="El link no es válido.")
        
        user_token = user.get_context_string(context=USER_VERIFY_ACCOUNT)
        try:
            token_valid = verify_password(user_token, data.token)
        except Exception as verify_exec:
            logging.exception(verify_exec)
            token_valid = False
        if not token_valid:
            raise HTTPException(status_code=400, detail="El link expiró o no es válido.")
        
        user.is_active = True
        user.updated_at = datetime.now(timezone.utc)
        user.verified_at = datetime.now(timezone.utc)
        session.add(user)
        session.commit()
        session.refresh(user)

        await send_account_activation_confirmation_email(user, background_tasks)
        
        return user
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,  
            content={"detail": str(e)} 
        )



async def get_login_token(data, session):

    """
    Genera un token de inicio de sesión tras validar las credenciales del usuario.

    Args:
        - data (UserLoginRequest): Contiene las credenciales del usuario (nombre de usuario y contraseña).
        - session (Session): Sesión de base de datos.

    Returns:
        - dict: Un diccionario con los tokens generados.

    Raises:
        - HTTPException 400: Si las credenciales son incorrectas, la cuenta no está verificada, o está desactivada.
        - HTTPException: Si ocurre un error relacionado con la solicitud HTTP.
        - Exception: Si ocurre un error inesperado durante la creación de la cuenta.
    """


    user = await load_user(data.username, session)
    if not user:
        raise HTTPException(status_code=400, detail="El correo electrónico no está registrado.")
    
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Correo electrónico o contraseña incorrectos.")
    
    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Tu cuenta no está verificada. Por favor, revisa tu bandeja de entrada para verificar tu cuenta.")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Tu cuenta ha sido desactivada. Por favor, contacta con soporte.")
        

    return _generate_tokens(user, session)



def _generate_tokens(user, session):
    """
    Genera y almacena tokens de acceso y actualización para el usuario.

    Args:
        - user (User): El usuario para el cual se están generando los tokens.
        - session (Session): La sesión de base de datos.

    Returns:
        - dict: Un diccionario que contiene el token de acceso (access_token), el token de actualización (refresh_token),
                y el tiempo de expiración del token de acceso en segundos.

    Raises:
        - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
        - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """


    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token = UserToken()
    user_token.user_id = user.id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.expires_at = datetime.now(timezone.utc) + rt_expires
    session.add(user_token)
    session.commit()
    session.refresh(user_token)

    at_payload = {

        "sub": str(user.id), 
        'a': access_key,
        'r': str_encode(str(user_token.id)),
        'n': str_encode(f"{user.username}")
    }

    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(at_payload, at_expires)

    rt_payload = {"sub": str_encode(str(user.id)), "t": refresh_key, 'a': access_key}
    refresh_token = generate_token(rt_payload, rt_expires)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds
    }
 
 
    
async def get_refresh_token(refresh_token, session):
    """
    Genera un nuevo token de acceso utilizando un token de actualización (refresh token).

    Args:
        - refresh_token (str): El token de actualización utilizado para generar un nuevo token de acceso.
        - session (Session): La sesión de base de datos.

    Returns:
        - dict: Un diccionario que contiene el nuevo token de acceso (access_token), el token de actualización (refresh_token),
                y el tiempo de expiración del token de acceso en segundos.

    Raises:
        - HTTPException 400: Si el token de actualización es inválido o ha expirado.
        - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
        - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """


    token_payload = decode_jwt(refresh_token)
    
    if not token_payload:
        raise HTTPException(status_code=400, detail="Respuesta inválida.")
    
    refresh_key = token_payload.get('t')
    access_key = token_payload.get('a')
    user_id = str_decode(token_payload.get('sub'))
    user_token = session.query(UserToken).options(joinedload(UserToken.user)).filter(UserToken.refresh_key == refresh_key,
                                                 UserToken.access_key == access_key,
                                                 UserToken.user_id == user_id,
                                                 UserToken.expires_at > datetime.now(timezone.utc)
                                                 ).first()
    if not user_token:
        raise HTTPException(status_code=400, detail="Respuesta inválida.")
    
    user_token.expires_at = datetime.now(timezone.utc)
    session.add(user_token)
    session.commit()
    return _generate_tokens(user_token.user, session)



async def email_forgot_password_link(data, background_tasks, session):
    """
    Envía un correo de restablecimiento de contraseña si el usuario está verificado y activo.

    Args:
        - data (ForgotPasswordRequest): Datos que contienen el correo electrónico del usuario que solicita el restablecimiento de la contraseña.
        - background_tasks (BackgroundTasks): Objeto para ejecutar tareas en segundo plano, como el envío de correos electrónicos.
        - session (Session): Sesión de base de datos.

    Returns:
        - None: Si se envía con éxito el correo de restablecimiento.

    Raises:
        - HTTPException 400: Si la cuenta del usuario no está verificada o está desactivada.
        - HTTPException: Si ocurre un error relacionado con la solicitud HTTP.
        - Exception: Si ocurre un error inesperado durante la creación de la cuenta.
    """

    try:
        
        user = await load_user(data.email, session)
        
        if not user:
            raise HTTPException(status_code=400, detail="El usuario no existe.")
                
        if not user.verified_at:
            raise HTTPException(status_code=400, detail="Tu cuenta no está verificada. Por favor, revisa tu bandeja de entrada para verificar tu cuenta.")
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Tu cuenta ha sido desactivada. Por favor, contacta con soporte.")
        
        await send_password_reset_email(user, background_tasks)
        
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,  
            content={"detail": str(e)} 
        )

  
  
       
    
async def reset_user_password(data, session):
    """
    Restablece la contraseña del usuario si el token es válido y el usuario está activo y verificado.

    Args:
        - data (ResetPasswordRequest): Datos que contienen el correo electrónico del usuario, el token de restablecimiento y la nueva contraseña.
        - session (Session): Sesión de base de datos.

    Returns:
        - dict: Un mensaje indicando que la contraseña ha sido restablecida con éxito.

    Raises:
        - HTTPException 400: Si el token es inválido, el usuario no está verificado, o el usuario no está activo.
        - HTTPException: Si ocurre un error relacionado con la solicitud HTTP.
        - Exception: Si ocurre un error inesperado durante la creación de la cuenta.
    """


    try:
        user = await load_user(data.email, session)
        
        if not user:
            raise HTTPException(status_code=400, detail="Respuesta inválida.")
            
        
        if not user.verified_at:
            raise HTTPException(status_code=400, detail="Respuesta inválida.")
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Respuesta inválida.")
        
        user_token = user.get_context_string(context=FORGOT_PASSWORD)
        try:
            token_valid = verify_password(user_token, data.token)
        except Exception as verify_exec:
            logging.exception(verify_exec)
            token_valid = False
        if not token_valid:
            raise HTTPException(status_code=400, detail="Respuesta inválida.")
        
        user.password = hash_password(data.password)
        user.updated_at = datetime.now()
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"message": "Contraseña restablecida con éxito."}

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,  
            content={"detail": str(e)} 
        )
   
   
    
async def fetch_user_detail(user_id, session):
    """
    Recupera los detalles del usuario por su ID.

    Args:
        - user_id (int): El ID del usuario a recuperar.
        - session (Session): Sesión de base de datos.

    Returns:
        - User: El objeto de usuario correspondiente al ID proporcionado.

    Raises:
        - UserNotFoundException: Si no se encuentra un usuario con el ID especificado.
        - HTTPException: Si ocurre un error relacionado con la solicitud HTTP.
        - Exception: Si ocurre un error inesperado durante la creación de la cuenta.
    """

    
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return user
        raise UserNotFoundException()
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,  
            content={"detail": str(e)} 
        )



async def update_user_account(data, session, current_user: User):
    """
    Actualiza la cuenta del usuario con los nuevos datos proporcionados.

    Args:
        - data (UserAccountUpdateRequest): Datos con la nueva información para actualizar la cuenta del usuario.
        - session (Session): Sesión de base de datos.
        - current_user (User): El usuario actualmente autenticado.

    Returns:
        - User: El usuario actualizado con los nuevos datos.

    Raises:
        - UserNotFoundException: Si no se encuentra el usuario en la base de datos.
        - HTTPException: Si ocurre un error relacionado con la solicitud HTTP.
        - Exception: Si ocurre un error inesperado durante la creación de la cuenta.
    """

    try:
        user = session.query(User).filter(User.id == current_user.id).first()
        
        if not user:
            raise UserNotFoundException()


        user.username = data.username
        user.updated_at = datetime.now(timezone.utc)


        session.commit()
        session.refresh(user)

        return user  
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,  
            content={"detail": str(e)} 
        )
    

async def delete_user_account(user_id: int, session):

    """
    Elimina la cuenta del usuario de manera lógica (marcando como eliminado).

    Args:
        - user_id (int): ID del usuario que se desea eliminar.
        - session (Session): Sesión de base de datos.

    Returns:
        - dict: Un diccionario con el ID del usuario, la fecha de eliminación y un mensaje de confirmación.

    Raises:
        - HTTPException 404: Si no se encuentra el usuario en la base de datos.
        - HTTPException 400: Si el usuario ya está marcado como eliminado.
        - HTTPException: Si ocurre un error relacionado con la solicitud HTTP.
        - Exception: Si ocurre un error inesperado durante la creación de la cuenta.
    """
    
    try:
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if user.deleted_at:
            raise HTTPException(status_code=400, detail="El usuario ya está eliminado")

        user.deleted_at = datetime.now(timezone.utc)


        user_profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        if user_profile:
            user_profile.deleted_at = user.deleted_at  

        session.commit()

        return user
        
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,  
            content={"detail": str(e)} 
        )