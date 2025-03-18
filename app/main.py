from fastapi import FastAPI
from app.api.api import api_router
from app.middlewares.authentication import AuthenticationMiddleware


app = FastAPI(title="Evoltronic Store API", version="1.0.0")

# Middleware de autenticación
app.add_middleware(AuthenticationMiddleware)
# Rutas de la aplicación
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hela Mundo"}



 