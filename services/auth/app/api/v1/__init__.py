from fastapi import APIRouter

from .routers.auth import router as auth_router

v1_router = APIRouter()
v1_router.include_router(auth_router, prefix='/auth')
