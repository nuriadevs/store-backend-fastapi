from typing import List
from fastapi import APIRouter, status,Depends, status
from app.core.database import get_session
from app.models.user.user import User
from app.responses.order import OrderResponse
from sqlalchemy.orm import Session
from app.schemas.order import OrderStatusUpdateRequest
from app.services.order.order import delete_user_order, fetch_all_order, fetch_order_id, patch_delete_order, update_order
from app.dependencies.admin import is_admin
from app.dependencies.user import get_current_user

admin_order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not Found"}},
)

   

@admin_order_router.get("/orders/", response_model=List[OrderResponse])
async def fetch_orders(session: Session = Depends(get_session), current_user: User = Depends(get_current_user),
    user=Depends(is_admin)):
    """
    Obtiene una lista de todos los pedidos registrados.

    Args:
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
       - List[OrderResponse]: Lista de pedidos registrados.
    """
    return await fetch_all_order(session)



@admin_order_router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
async def fetch_order_detail_id(order_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user), user=Depends(is_admin)
    ):

    """
    Obtiene los detalles de un pedido específico por su ID.

    Args:
       - order_id (int): ID del pedido a consultar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
       - OrderResponse: Información del pedido solicitado.
    """    

    return await fetch_order_id(order_id, session)



@admin_order_router.delete("/{order_id}",  response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def delete_order_id(
    order_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
):

    """
    Elimina un pedido de la base de datos si esta marcado como pendiente.

    Args:
       - order_id (int): ID del pedido a eliminar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.
       - user: Usuario autenticado con permisos de administrador.

    Returns:
       - Response: Mensaje confirmando la eliminación del pedido.
    """
    

    return await delete_user_order(order_id, session)


@admin_order_router.patch("/{order_id}/delete", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def delete_order(order_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)
   ):
    """
    Realiza un borrado lógico de un pedido marcándolo como eliminado.
    El cliente puede marcar como eliminado su pedido con estado "pendiente".

    Args:
       - order_id (int): ID del pedido a eliminar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.
       - current_user: Usuario autenticado que realiza la acción.

    Returns:
       - OrderResponse: Información del pedido actualizado.
    """
    return await patch_delete_order(order_id, session, current_user)


@admin_order_router.patch("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def update_order_route(
    order_id: int,
    data: OrderStatusUpdateRequest,  
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    user=Depends(is_admin)
):
    """
    Actualiza el estado de un pedido específico.

    Args:
       - order_id (int): ID del pedido a actualizar.
       - data (OrderStatusUpdateRequest): Datos del nuevo estado del pedido.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.
       - user: Usuario autenticado con permisos de administrador.

    Returns:
       - OrderResponse: Información del pedido actualizado.
    """
    return await update_order(order_id, session, data.dict())
