from fastapi import APIRouter
from app.api.routes.client.profile_router import profile_router
from app.api.routes.admin.admin_profile_router import admin_profile_router
from app.api.routes.auth.guest_routes import guest_router
from app.api.routes.client.user_routes import user_router
from app.api.routes.admin.admin_user_router import admin_user_router
from app.api.routes.admin.admin_product_routes import admin_product_router
from app.api.routes.client.product_routes import product_router
from app.api.routes.admin.admin_category_routes import admin_category_router
from app.api.routes.client.category_routes import category_router
from app.api.routes.admin.admin_order_routes import admin_order_router
from app.api.routes.client.order_routes import order_router
from app.api.routes.public.hello import public_router

api_router = APIRouter()
#Auth
api_router.include_router(guest_router)
#User
api_router.include_router(user_router)
api_router.include_router(admin_user_router)
#Profile
api_router.include_router(profile_router)
api_router.include_router(admin_profile_router)
#Products
api_router.include_router(product_router)
api_router.include_router(admin_product_router)
#Categories
api_router.include_router(category_router)
api_router.include_router(admin_category_router)
#Orders
api_router.include_router(order_router)
api_router.include_router(admin_order_router)
#Public
api_router.include_router(public_router)