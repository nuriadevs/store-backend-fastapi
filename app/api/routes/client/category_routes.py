from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.user.user import User
from app.responses.category import  CategoryResponse
from app.services.category.category import fetch_all_category, fetch_category_id
from app.dependencies.user import get_current_user


category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Not Found"}},
)

  


@category_router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def fetch_category_detail_id(category_id: int, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    """
    Obtiene los detalles de una categoría específica por su ID.

    Args:
       - category_id (int): ID de la categoría a consultar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
       - CategoryResponse: Información de la categoría solicitada.
    """
    return await fetch_category_id(category_id, session)

    
@category_router.get("/categories/", response_model=List[CategoryResponse])
async def fetch_categories(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Obtiene una lista de todas las categorías registradas.

    Args:
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
       - List[CategoryResponse]: Lista de categorías registradas.
    """
    return await fetch_all_category(session)

