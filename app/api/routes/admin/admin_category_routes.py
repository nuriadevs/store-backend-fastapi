
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.user.user import User
from app.responses.category import CategoryDeleteResponse, CategoryUpdateResponse
from app.schemas.category import CategoryCreateRequest
from app.services.category.category import create_category, delete_category, update_categpry_id
from app.dependencies.admin import is_admin
from app.dependencies.user import get_current_user


admin_category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Not Found"}},
)


@admin_category_router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_category_route(
   data: CategoryCreateRequest, 
   session: Session = Depends(get_session), 
   current_user: User = Depends(get_current_user),
   user=Depends(is_admin)
):
    """
    Crea una nueva categoría en la base de datos.

    Args:
       - data (CategoryCreateRequest): Datos de la categoría a registrar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.
       - user: Usuario autenticado con permisos de administrador.

    Returns:
       - CategoryResponse: Información de la categoría creada.
    """
    return await create_category(session, data)


@admin_category_router.patch("/{category_id}", response_model=CategoryUpdateResponse,status_code=status.HTTP_200_OK)
async def update_category_route(
    category_id: int,
    category_data: CategoryCreateRequest,  
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
):
    """
    Actualiza la información de una categoría específica.

    Args:
       - category_id (int): ID de la categoría a actualizar.
       - category_data (CategoryCreateRequest): Nuevos datos de la categoría.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
       - CategoryUpdateResponse: Información de la categoría actualizada.
    """
    return await update_categpry_id(category_id, session, category_data)


@admin_category_router.delete("/{category_id}", response_model=CategoryDeleteResponse)
async def delete_category_route(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
):
    """
    Elimina una categoría de la base de datos.

    Args:
       - category_id (int): ID de la categoría a eliminar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
       - CategoryDeleteResponse: Información de la categoría eliminada.
    """
    return await delete_category(category_id, session)