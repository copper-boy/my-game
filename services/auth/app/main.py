import logging
from asyncio import sleep

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from tortoise.contrib.fastapi import register_tortoise

from app.api import api_router
from app.schemas.auth import AuthSchema
from app.settings.config import (JWTSettingsSchema, get_admin_settings,
                                 get_database_settings)
from app.settings.handlers import register_all_exception_handlers
from app.utils.admin import create_admin
from app.utils.auth import authenticate_user, register_user


@AuthJWT.load_config
def load_config():
    return JWTSettingsSchema()


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router, prefix='/api')

    register_all_exception_handlers(application)

    return application


app = create_application()


@app.get('/')
async def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            'ping': 'pong'
                        })


@app.on_event('startup')
async def startup() -> None:
    await register_admin()


async def setup_admin() -> None:
    config = get_admin_settings()
    try:
        user = await register_user(config.ADMIN_LOGIN,
                                   config.ADMIN_PASSWORD)
    except HTTPException:
        user = await authenticate_user(AuthSchema(email=config.ADMIN_LOGIN,
                                                  password=config.ADMIN_PASSWORD))
    _unused = await create_admin(user)


async def register_admin() -> None:
    while True:
        try:
            await setup_admin()
        except TypeError:
            logging.info('wait for tortoise setup')
            await sleep(5)
        else:
            break

register_tortoise(app,
                  db_url=get_database_settings().AUTH_DATABASE_URI,
                  modules={
                      'models': ['app.orm.user']
                  },
                  generate_schemas=True,
                  add_exception_handlers=True)
