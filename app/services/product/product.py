from datetime import datetime, timezone
from decimal import Decimal
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import DatabaseErrorException, ProductNotFoundException, UnexpectedErrorException
from app.models.category.category import  Category
from app.models.product.product import Product
from app.responses.product import ProductResponse
from sqlalchemy.exc import SQLAlchemyError
import logging



async def create_product(session, product_data):
    """Crea un nuevo producto en la base de datos si no existe uno con el mismo nombre y categoría.

    Args:
       - session (Session): Sesión de base de datos.
       - product_data (ProductCreateRequest): Datos del producto a crear.

    Returns:
       - Product: Producto recién creado.

    Raises:
       - HTTPException 400: Si el producto ya existe o la categoría no es válida.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    
    try:
        category = session.query(Category).filter(Category.id == product_data.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Categoría no existe")
        

        existing_product = session.query(Product).filter(Product.name == product_data.name).first()
        
        if existing_product:
            raise HTTPException(status_code=400, detail="El producto ya existe")

        price = Decimal(str(product_data.price)) 

        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=price,
            stock=product_data.stock,
            category_id=product_data.category_id
        )


        session.add(new_product)
        session.commit()
        session.refresh(new_product)
            
        return new_product

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



async def fetch_product_id(product_id, session):
    """Obtiene un producto de la base de datos por su ID.

    Args:
       - product_id (int): ID del producto.
       - session (Session): Sesión de base de datos.

    Returns:
       - Product: Producto con el ID especificado.

    Raises:
       - ProductNotFoundException: Si no se encuentra el producto.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:    
        product = session.query(Product).filter(Product.id == product_id).first()

        if product:
            return product
        else: 
            print(f"Resultado get product: ", product)
        
        raise ProductNotFoundException()

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


async def fetch_all_products(session):
    """Obtiene todos los productos de la base de datos.

    Args:
       - session (Session): Sesión de base de datos.

    Returns:
       - List[Product]: Lista de productos.

    Raises:
       - ProductNotFoundException: Si no se encuentran productos.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """
 
    try:
        products = session.query(Product).all()
        
        if products:
            return products
        else:
            raise ProductNotFoundException()

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
    
    

async def update_product(product_id: int, session, data: dict):
    """
    Actualiza un producto con los datos proporcionados.

    Args:
       - product_id (int): ID del producto a actualizar.
       - session (Session): Sesión de base de datos.
       - data (dict): Datos a actualizar en el producto.

    Returns:
       - ProductResponse: Producto actualizado.

    Raises:
       - HTTPException 404: Si el producto no existe.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:
        product = session.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        for key, value in data.items():
            if value is not None:  
                setattr(product, key, value)

        product.updated_at = datetime.now()


        session.commit()
        session.refresh(product)

        return ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category_id=product.category_id
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


async def delete_product(product_id,session):
    """
    Realiza el borrado lógico del producto, marcando `deleted_at` con la fecha actual.

    Args:
       - product_id (int): ID del producto a eliminar.
       - session (Session): Sesión de base de datos.

    Returns:
       - ProductResponse: Producto eliminado con la fecha de eliminación.

    Raises:
       - HTTPException 404: Si el producto no se encuentra.
       - HTTPException 404: Si no se encuentra el token de usuario correspondiente en la base de datos.
       - Exception: Si ocurre un error inesperado durante el proceso de obtención del nuevo token.
    """

    try:
        product = session.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Order not found.")
            

        deleted_product = ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=float(product.price),  
            stock=product.stock,
            category_id=product.category_id,
             deleted_at=datetime.now(timezone.utc)
        )

        product.deleted_at = datetime.now(timezone.utc)
        session.commit()

        return deleted_product

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