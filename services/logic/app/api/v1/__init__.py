from fastapi import APIRouter

from .routers.game import router as game_router
from .routers.session import router as session_router

v1_router = APIRouter()
v1_router.include_router(game_router, prefix='/logic')
v1_router.include_router(session_router, prefix='/logic')
