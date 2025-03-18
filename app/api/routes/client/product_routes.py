from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.responses.product import ProductResponse
from app.services.product.product import fetch_all_products, fetch_product_id


product_router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not Found"}},
)


@product_router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def fetch_product_info_id(product_id: int, session: Session = Depends(get_session)):
    """
    Obtiene los detalles de un producto específico por su ID.

    Args:
       - product_id (int): ID del producto a consultar.
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
       - ProductResponse: Información del producto solicitado.
    """    
    return await fetch_product_id(product_id, session)

    
@product_router.get("/products/", response_model=List[ProductResponse])
async def fetch_products(session: Session = Depends(get_session)):
    """
    Obtiene la lista de todos los productos disponibles.

    Args:
       - session (Session): Sesión de base de datos obtenida mediante inyección de dependencias.

    Returns:
       - List[ProductResponse]: Lista de productos registrados.
    """
    return await fetch_all_products(session)

    
