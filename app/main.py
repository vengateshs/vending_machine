from fastapi import FastAPI
from app.api.api import api_router
from app.middlewares.auth import auth_middleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title="Vending Machine Service")

app.include_router(api_router)

app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)