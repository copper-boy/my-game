from asyncio import ensure_future, get_event_loop

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from tortoise.contrib.fastapi import register_tortoise

from api import api_router
from utils.admin import create_admin
from utils.auth import register_user
from settings.config import JWTSettingsSchema, get_database_settings
from settings.handlers import register_all_exception_handlers
from settings.middlewares import setup_middlewares
from settings.rabbitmq import consume


@AuthJWT.load_config
def load_config():
    return JWTSettingsSchema()


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router, prefix='/api')

    register_all_exception_handlers(application)
    setup_middlewares(application)

    return application


app = create_application()


@app.on_event('startup')
async def startup() -> None:
    loop = get_event_loop()
    ensure_future(consume(loop))


register_tortoise(app,
                  db_url=get_database_settings().AUTH_DATABASE_URI,
                  modules={
                      'models': ['orm.user']
                  },
                  generate_schemas=True,
                  add_exception_handlers=True)

