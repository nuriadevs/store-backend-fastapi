from typing import List
from fastapi import APIRouter, status,Depends, status
from app.core.database import get_session
from app.models.user.user import User
from app.responses.order import OrderResponse
from sqlalchemy.orm import Session
from app.schemas.order import CreateOrderRequest
from app.services.order.order import create_order, fetch_all_order, fetch_order_id, fetch_user_orders, patch_delete_order, update_order
from app.dependencies.user import get_current_user

order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not Found"}},
)


@order_router.post("/create/", response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
async def create_order_route(
    order_data: CreateOrderRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Crea un nuevo pedido en la base de datos.

    Args:
       - order_data (CreateOrderRequest): Datos del pedido a registrar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
       - OrderResponse: Información del pedido creado.
    """
    return await create_order(order_data, session)


@order_router.get("/me", status_code=status.HTTP_200_OK, response_model=List[OrderResponse])
async def fetch_order_user( 
orders=Depends(fetch_user_orders)
):
    """
    Permite que un usuario autenticado obtenga sus pedidos.

    Args:
       - user (User): El usuario autenticado. Se obtiene mediante la inyección de dependencias usando el `Depends(get_current_user)`.

    Returns:
       - orders: Los detalles del los pedidos del usuario autenticado.
    """
    return orders

 



