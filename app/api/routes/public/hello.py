from fastapi import APIRouter


public_router = APIRouter(
    prefix="/index",
    tags=["Public"],
    responses={404: {"description": "Not Found"}},
)

@public_router.get("/")
async def root():
    return {"message": "Hello World, I'm Evoltronic store."}