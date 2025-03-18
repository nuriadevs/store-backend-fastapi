from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.user.user import User
from app.responses.product import ProductResponse
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest
from app.services.product.product import create_product, delete_product, update_product
from app.dependencies.admin import is_admin
from app.dependencies.user import get_current_user


admin_product_router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not Found"}},
)


@admin_product_router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_product_route(data: ProductCreateRequest, 
                               session: Session = Depends(get_session), 
                               current_user: User = Depends(get_current_user),
                               user=Depends(is_admin)
):
    """
    Crea un nuevo producto en la base de datos.

    Args:
       - data (ProductCreateRequest): Datos del producto a crear.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.
       - user: Usuario autenticado con permisos de administrador.

    Returns:
       - ProductResponse: Información del producto creado.
    """
        
    return await create_product(session, data)


@admin_product_router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product_route(
    product_id: int,
    data: ProductUpdateRequest,  
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
):
    """
    Actualiza la información de un producto específico.

    Args:
       - product_id (int): ID del producto a actualizar.
       - data (ProductUpdateRequest): Datos del producto a modificar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.
       - user: Usuario autenticado con permisos de administrador.

    Returns:
       - ProductResponse: Información del producto actualizado.
    """
    return await update_product(product_id, session, data.dict())



@admin_product_router.delete("/products/{product_id}", response_model=ProductResponse)
async def update_product_route(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
):
    """
    Elimina un producto de la base de datos.

    Args:
       - product_id (int): ID del producto a eliminar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.
       - user: Usuario autenticado con permisos de administrador.

    Returns:
       - dict: Mensaje confirmando la eliminación del producto.
    """
    return await delete_product(product_id, session)
