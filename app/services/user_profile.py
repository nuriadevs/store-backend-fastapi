from datetime import datetime, timezone
import logging
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import UserNotFoundException
from app.core.security import dni_valid
from app.models.user.user_profile import UserProfile
from app.schemas.user_profile import UserProfileUpdateAdressRequest



async def create_user_profile(data, session, current_user):

    """
    Crea un perfil de usuario autenticado.

    Args:
       - data (UserProfileCreateRequest): Datos para crear el perfil de usuario.
       - session (Session): Sesión de base de datos.
       - current_user (User): El usuario actualmente autenticado.

    Returns:
       - UserProfile: El perfil de usuario recién creado.

    Raises:
       - HTTPException 400: Si el perfil de usuario ya existe.
        - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
        - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:
        existing_profile = session.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if existing_profile:
            raise HTTPException(status_code=400, detail="User profile already exists")
        
        if not dni_valid(data.dni):
            raise HTTPException(status_code=400, detail="DNI inválido")

        user_profile = UserProfile(
            user_id=current_user.id,
            first_name=data.first_name,
            last_name=data.last_name,
            dni=data.dni,
            phone=data.phone,
            address=data.address,
            birth_date=data.birth_date,
            city=data.city,
            zip_code=data.zip_code,
        )

        session.add(user_profile)
        session.commit()
        session.refresh(user_profile)
        
        return user_profile
    
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


  
async def update_user_profile(data, session, current_user):

    """
    Actualiza solo el perfil del usuario en UserProfile.

    Args:
       - data (UserProfileUpdateRequest): Datos a actualizar del perfil del usuario.
       - session (Session): Sesión de base de datos.
       - current_user (User): El usuario actualmente autenticado.

    Returns:
       - dict: Mensaje de éxito y el perfil actualizado.

    Raises:
        - UserNotFoundException: Si el perfil del usuario no se encuentra.
        - DatabaseErrorException: Si ocurre un error en la base de datos.
        - UnexpectedErrorException: Si ocurre un error inesperado.
    """


    try:
        existing_profile = session.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

        if not existing_profile:
            raise UserNotFoundException()
        
        if not dni_valid(data.dni):
            raise HTTPException(status_code=400, detail="DNI inválido")

        existing_profile.first_name = data.first_name
        existing_profile.last_name = data.last_name
        existing_profile.dni = data.dni
        existing_profile.phone = data.phone
        existing_profile.address = data.address
        existing_profile.birth_date = data.birth_date
        existing_profile.city = data.city
        existing_profile.zip_code = data.zip_code
        existing_profile.updated_at = datetime.now(timezone.utc)


        session.commit()
        session.refresh(existing_profile)

        return {
            "message": "Perfil actualizado correctamente",
            "profile": existing_profile
        }
        
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


async def update_user_address(data: UserProfileUpdateAdressRequest, session, current_user):

    """
    Actualiza la dirección, ciudad y código postal del perfil de usuario.

    Args:
       - data (UserProfileUpdateAdressRequest): Datos de la nueva dirección, ciudad y código postal.
       - session (Session): Sesión de base de datos.
       - current_user (User): El usuario actualmente autenticado.

    Returns:
       - dict: Mensaje de éxito con el nombre del usuario.

    Raises:
        - HTTPException 404: Si el perfil de usuario no se encuentra.
        - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
        - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:
        user_profile = session.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not encontrado")

        if data.address:
            user_profile.address = data.address
        if data.city:
            user_profile.city = data.city
        if data.zip_code:
            user_profile.zip_code = data.zip_code

        user_profile.updated_at = datetime.now(timezone.utc)  
        session.commit()
        session.refresh(user_profile)

        return {"message": f"User profile {user_profile.first_name} address actualizado correctamente"}
    
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

async def get_user_profile(user_id, session):
    """
    Recupera el perfil del usuario a partir de su ID.

    Args:
       - user_id (int): ID del usuario cuyo perfil se desea recuperar.
       - session (Session): Sesión de base de datos.

    Returns:
       - UserProfile: Perfil del usuario encontrado.

    Raises:
        - HTTPException 404: Si el perfil del usuario no se encuentra.
        - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
        - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """
    try:
        # Intentamos recuperar el perfil del usuario
        user_profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not user_profile:
            # Si no se encuentra el perfil, lanzamos la excepción 404
            logging.warning(f"Perfil no encontrado para el usuario con ID {user_id}")
            raise HTTPException(status_code=404, detail="El perfil del usuario no fue encontrado")

        # Si el perfil existe, lo devolvemos
        return user_profile

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



async def delete_user_profile(user_id, session):
    """
    Realiza el borrado lógico del perfil de usuario, marcando `deleted_at` con la fecha actual.

    Args:
       - user_id (int): ID del usuario cuyo perfil se eliminará.
       - session (Session): Sesión de base de datos.

    Returns:
       - dict: Mensaje indicando que el perfil del usuario fue eliminado correctamente.

    Raises:
        - UserNotFoundException: Si el perfil de usuario no se encuentra.
        - HTTPException 400: Si el perfil de usuario ya ha sido eliminado.
        - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
        - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:
        user_profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()

        if not user_profile:
            raise UserNotFoundException()
        
        if user_profile.deleted_at is not None:
            raise HTTPException(status_code=400, detail="El perfil de usuario ya ha sido eliminado") 


        user_profile.deleted_at = datetime.now(timezone.utc)
        session.commit()

        return user_profile
    
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