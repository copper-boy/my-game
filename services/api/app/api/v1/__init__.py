from fastapi import APIRouter

from .routers.game import router as game_router

v1_router = APIRouter()
v1_router.include_router(game_router, prefix='/admin')
