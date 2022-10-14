from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from tortoise.contrib.fastapi import register_tortoise

from app.api import api_router
from app.settings.config import JWTSettingsSchema, get_database_settings
from app.settings.handlers import register_all_exception_handlers


@AuthJWT.load_config
def load_config():
    return JWTSettingsSchema()


def create_application() -> FastAPI:
    application = FastAPI(title='Auth',
                          openapi_url='/api/openapi.json',
                          docs_url='/api/docs',
                          redoc_url='/api/redoc')
    application.include_router(api_router, prefix='/api', tags=['API'])

    register_all_exception_handlers(application)

    return application


app = create_application()


@app.get('/')
async def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            'ping': 'pong'
                        })


register_tortoise(app,
                  db_url=get_database_settings().AUTH_DATABASE_URI,
                  modules={
                      'models': ['app.orm.user']
                  },
                  generate_schemas=True,
                  add_exception_handlers=True)
