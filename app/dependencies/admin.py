from fastapi import Request,HTTPException


async def is_admin(request: Request):
    """
    Verifica si el usuario tiene el rol de administrador. Si no, lanza un error.
    """

    user = getattr(request.state, "user", None)

    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")


    if not user.roles:  
        raise HTTPException(status_code=403, detail="El usuario no tienen rol asignado")

    
    if not any(role.name == "admin" for role in user.roles):
        raise HTTPException(status_code=403, detail="Acceso denegado: Solo para administradores.")

    return user

