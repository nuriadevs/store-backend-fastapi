from datetime import datetime
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from pytest import Session
from app.core.database import get_session
from app.core.exceptions import DatabaseErrorException, UnexpectedErrorException
from app.models.order.order import Order
from app.models.order.order_item import OrderItem
from app.models.product.product import Product
from app.models.user.user import User
from app.responses.order import OrderItemResponse, OrderResponse
from app.schemas.order import CreateOrderRequest
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.dependencies.user import get_current_user



async def create_order( order_data: CreateOrderRequest, session: Session):
    """Crea un nuevo pedido y asocia productos existentes al mismo.

    Args:
       - order_data (CreateOrderRequest): Datos del pedido.
       - session (Session): Sesión de base de datos.

    Returns:
       - OrderResponse: Respuesta con los detalles del pedido creado.

    Raises:
       - HTTPException 404: Si algún producto no es encontrado.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:

        order = Order(user_id=order_data.user_id, status="pendiente", total_price=0)
        session.add(order)
        session.commit()
        session.refresh(order)


        total_price = 0
        order_items_response = []


        for product_data in order_data.products:
            product = session.query(Product).filter(Product.id == product_data.product_id).first()

            if not product:
                raise HTTPException(status_code=404, detail=f"Product with ID {product_data.product_id} not found.")


            subtotal = product.price * product_data.quantity
            order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=product_data.quantity, subtotal=subtotal)
            session.add(order_item)
            total_price += subtotal


            order_items_response.append(OrderItemResponse(
                product_id=product.id,
                name=product.name,  
                quantity=product_data.quantity,
                subtotal=subtotal
            ))


        order.total_price = total_price
        session.commit()


        return OrderResponse(
            id=order.id,
            user_id=order.user_id,
            total_price=order.total_price,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            order_items=order_items_response
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


async def fetch_order_id(order_id,session: Session = Depends(get_session)):

    """Obtiene los detalles de un pedido por su ID, incluyendo los productos asociados.

    Args:
       - order_id (int): ID del pedido a obtener.
       - session (Session): Sesión de base de datos.

    Returns:
       - OrderResponse: Respuesta con los detalles del pedido.

    Raises:
       - HTTPException 404: Si no se encuentra el pedido.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """
 
    try:
        order = session.query(Order).filter(Order.id == order_id, Order.deleted_at == None).first()

        
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        
        order_items_response = []
        

        for order_item in order.order_items:
            order_items_response.append(OrderItemResponse(
                product_id=order_item.product_id,
                name=order_item.product.name,  
                quantity=order_item.quantity,
                subtotal=order_item.subtotal
            ))


        order_response = OrderResponse(
            id=order.id,
            user_id=order.user_id,
            total_price=order.total_price,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            order_items=order_items_response
        )
        
        return order_response

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


async def fetch_user_orders(session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    """
    Obtiene todos los pedidos asociados al usuario autenticado.

    Args:
       - session (Session): Sesión de base de datos.
       - current_user (User): Usuario autenticado.

    Returns:
       - List[OrderResponse]: Lista de pedidos del usuario autenticado.

    Raises:
       - HTTPException 404: Si el usuario no tiene pedidos.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """
    try:
        # Filtramos los pedidos por el `user_id` del usuario autenticado
        orders = session.query(Order).filter(Order.user_id == current_user.id, Order.deleted_at == None).all()

        # Si no hay pedidos asociados al usuario, lanzamos un error 404
        if not orders:
            raise HTTPException(status_code=404, detail="No tienes pedidos registrados.")

        order_responses = []
        
        for order in orders:
            order_items_response = [
                OrderItemResponse(
                    product_id=item.product_id,
                    name=item.product.name,  
                    quantity=item.quantity,
                    subtotal=item.subtotal
                ) for item in order.order_items
            ]

            # Creamos el response de cada pedido
            order_responses.append(OrderResponse(
                id=order.id,
                user_id=order.user_id,
                total_price=order.total_price,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
                order_items=order_items_response
            ))

        return order_responses
    
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



async def fetch_all_order(session: Session = Depends(get_session)):
    """Obtiene todos los pedidos no eliminados de la base de datos, junto con sus productos asociados.

    Args:
       - session (Session): Sesión de base de datos.

    Returns:
       - List[OrderResponse]: Lista de respuestas con los detalles de los pedidos.

    Raises:
       - HTTPException 404: Si no se encuentran pedidos.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """
    
    try:
        orders = session.query(Order).filter(Order.deleted_at == None).all()  
        
        if not orders:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        
        order_responses = []
        for order in orders:
            order_items_response = []

            for order_item in order.order_items:
                order_items_response.append(OrderItemResponse(
                    product_id=order_item.product_id,
                    name=order_item.product.name,  
                    quantity=order_item.quantity,
                    subtotal=order_item.subtotal
                ))
            

            order_responses.append(OrderResponse(
                id=order.id,
                user_id=order.user_id,
                total_price=order.total_price,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
                order_items=order_items_response
            ))
        
        return order_responses
    
    
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



async def delete_user_order(order_id,session: Session = Depends(get_session)):
    """Realiza el borrado lógico de un pedido y de todos los items relacionados, marcando `deleted_at` con la fecha actual.

    Args:
       - order_id (int): ID del pedido a eliminar.
       - session (Session): Sesión de base de datos.

    Returns:
       - dict: Mensaje indicando el éxito de la operación.

    Raises:
       - HTTPException 404: Si no se encuentra el pedido.
       - HTTPException 400: Si el pedido no está en estado "pendiente".
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:
        order  = session.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        

        if order.status != "pendiente":
            raise HTTPException(status_code=400, detail="Solo pedidos pendientes pueden ser eliminados.")
        

        for order_item in order.order_items:
            order_item.deleted_at = datetime.now()  
            session.add(order_item)  
        
        order.status = "eliminado"
        order.deleted_at = datetime.now()
        session.commit()

        order_response = OrderResponse(
                id=order.id,
                user_id=order.user_id,
                total_price=order.total_price,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
                deleted_at=order.deleted_at,
                order_items=[
                    OrderItemResponse(
                        product_id=item.product_id,
                        name=item.product.name if item.product else "Producto desconocido",  
                        quantity=item.quantity,
                        subtotal=item.subtotal
                    )
                    for item in order.order_items
                ]
            )

        return order_response

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


async def patch_delete_order(order_id: int, session: Session = Depends(get_session), current_user = Depends(get_current_user)):

    """Elimina lógicamente un pedido y sus ítems si el pedido está en estado "pendiente" y es propiedad del cliente.

    Args:
       - order_id (int): ID del pedido a eliminar.
       - session (Session): Sesión de base de datos.
       - current_user (User): Usuario autenticado que intenta eliminar el pedido.

    Returns:
       - JSONResponse: Mensaje indicando el éxito de la eliminación.

    Raises:
       - HTTPException 404: Si el pedido no es encontrado.
       - HTTPException 400: Si el pedido no está en estado "pendiente".
       - HTTPException 403: Si el pedido no es propiedad del usuario actual.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """


    try:
        order = session.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")


        if order.status != "pendiente":
            raise HTTPException(status_code=400, detail="Solo los pedidos pendientes pueden ser eliminados.")

        if order.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Solo puedes eliminar tus propios pedidos.")

        order.status = "eliminado"
        order.deleted_at = datetime.now()
        
        for order_item in order.order_items:
            order_item.deleted_at = datetime.now()     
        

        session.commit()

        order_response = OrderResponse(
                id=order.id,
                user_id=order.user_id,
                total_price=order.total_price,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
                deleted_at=order.deleted_at,
                order_items=[
                    OrderItemResponse(
                        product_id=item.product_id,
                        name=item.product.name if item.product else "Producto desconocido",  
                        quantity=item.quantity,
                        subtotal=item.subtotal
                    )
                    for item in order.order_items
                ]
            )

        return order_response


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


async def update_order(order_id: int, session, data: dict):

    """Actualiza el estado de un pedido con los datos proporcionados.

    Args:
       - order_id (int): ID del pedido a actualizar.
       - session (Session): Sesión de base de datos.
       - data (dict): Datos a actualizar, específicamente el estado del pedido.

    Returns:
       - OrderResponse: Detalles del pedido actualizado, incluyendo sus ítems.

    Raises:
       - HTTPException 404: Si el pedido no es encontrado o ha sido marcado como eliminado.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """


    try:
        order = session.query(Order).filter(Order.id == order_id, Order.deleted_at == None).first()
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        if "status" in data and data["status"]:
            order.status = data["status"]

        order.updated_at = datetime.now()

        session.commit()
        session.refresh(order)

        order_items_response = []
        for order_item in order.order_items:
            order_items_response.append(OrderItemResponse(
                product_id=order_item.product_id,
                name=order_item.product.name,
                quantity=order_item.quantity,
                subtotal=order_item.subtotal
            ))

        return OrderResponse(
            id=order.id,
            user_id=order.user_id,
            total_price=order.total_price,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            order_items=order_items_response
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
