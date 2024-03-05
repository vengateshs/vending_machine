from fastapi import APIRouter

from app.api.routers import users
from app.api.routers import products
from app.api.routers import actions

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])
api_router.include_router(products.router, tags=["products"])
api_router.include_router(actions.router, tags=["actions"])