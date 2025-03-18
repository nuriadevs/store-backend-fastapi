from fastapi.responses import JSONResponse
from pytest import Session
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from app.core.database import get_session
from app.dependencies.user import get_current_user


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
        Este método se ejecuta en cada solicitud entrante y verifica la validez del token.
        
        Args:
            request (Request): El objeto de la solicitud que contiene la información de la solicitud HTTP.
            call_next (Callable): Una función para llamar al siguiente middleware o controlador de la solicitud.
        
        Returns:
            response (Response): Respuesta que se genera después de pasar por este middleware.
        
        Raises:
            HTTPException: Si el token es inválido o falta el ID de usuario en el token, se lanza una excepción HTTP 401.
    
    """
    async def dispatch(self, request: Request, call_next):

        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(request)  
        token = auth_header.split(" ")[1]  

        session: Session = next(get_session()) 

        try:

            user = await get_current_user(token, session)
            request.state.user = user  
        
       # except HTTPException as e:
       #     session.rollback() 
       #     print(f"Excepción en autenticación: {e.detail}")
       #     raise e
       # except Exception as e:
       #     session.rollback()  
       #     raise HTTPException(status_code=401, detail="No autenticado")
       
        except HTTPException as e:
            # Aquí es donde capturamos la excepción y la devolvemos con un código adecuado
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except Exception as e:
            # Manejo de errores generales
            return JSONResponse(
                status_code=401,
                content={"detail": "No autenticado"}
            )
        

        response = await call_next(request)
        return response