
from datetime import datetime, timezone
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import CategoryNotFoundException, DatabaseErrorException, UnexpectedErrorException
from app.models.category.category import  Category
from app.responses.category import  CategoryDeleteResponse, CategoryUpdateResponse
from app.schemas.category import CategoryCreateRequest
from sqlalchemy.exc import SQLAlchemyError
import logging



async def create_category(session, category_data: CategoryCreateRequest):
    """
    Crea una nueva categoría en la base de datos si no existe una con el mismo nombre.

    Args:
       - session (Session): Sesión de base de datos.
       - category_data (CategoryCreateRequest): Datos de la categoría.

    Returns:
       - Category: Categoría recién creada.
    
    Raises:
       - HTTPException 400: Si la categoría ya existe en la base de datos.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.        
    """
    try:
        
        existing_category = session.query(Category).filter(Category.name == category_data.name).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Categoría existe.")
        new_category = Category(
            name=category_data.name,
            description=category_data.description
        )

        session.add(new_category)
        session.commit()
        session.refresh(new_category)   
            
        return new_category
    
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


async def fetch_category_id(category_id, session):
    """Obtiene una categoría de la base de datos según su ID.

    Args:
       - category_id (int): ID de la categoría.
       - session (Session): Sesión de base de datos.

    Returns:
       - Category: Categoría encontrada.

    Raises:
       - CategoryNotFoundException: Si no se encuentra la categoría.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """
 
    try:
        
        category = session.query(Category).filter(Category.id == category_id).first()

        if category:
            return category
        else: 
            print(f"Resultado get category: ", category)
        
        raise CategoryNotFoundException()

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


async def fetch_all_category(session):
    """Obtiene todas las categorías de la base de datos.

    Args:
       - session (Session): Sesión de base de datos.

    Returns:
       - list: Lista de categorías.

    Raises:
       - CategoryNotFoundException: Si no se encuentran categorías.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:
        categories = session.query(Category).all()
        
        if categories:
            return categories
        else:
            raise CategoryNotFoundException()

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
    
    
    
async def update_categpry_id(category_id, session,category_data: CategoryCreateRequest):
    
    """Actualiza los datos de una categoría existente.

    Args:
       - category_id (int): ID de la categoría a actualizar.
       - session (Session): Sesión de base de datos.
       - category_data (CategoryCreateRequest): Nuevos datos de la categoría.

    Returns:
       - CategoryUpdateResponse: Respuesta con los datos actualizados de la categoría.

    Raises:
       - HTTPException 404: Si no se encuentra la categoría.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:
        category = session.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        
        category.name = category_data.name
        category.description= category_data.description
        category.updated_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(category)


        return CategoryUpdateResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            updated_at=category.updated_at
        )

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


async def delete_category(category_id,session):
    
    """Realiza el borrado lógico de una categoría, marcando `deleted_at` con la fecha actual.

    Args:
       - category_id (int): ID de la categoría a eliminar.
       - session (Session): Sesión de base de datos.

    Returns:
       - CategoryDeleteResponse: Respuesta con los datos de la categoría eliminada.

    Raises:
       - HTTPException 404: Si no se encuentra la categoría.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:
        category = session.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
            
        deleted_category = CategoryDeleteResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            deleted_at=datetime.now(timezone.utc)
        )

        category.deleted_at = datetime.now(timezone.utc)
        session.commit()

        return deleted_category 

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