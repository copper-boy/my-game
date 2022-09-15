from fastapi import FastAPI
from fastapi.param_functions import Query, Header
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

from app.api import api_router
from app.settings.config import get_database_settings
from app.settings.handlers import register_all_exception_handlers
from app.settings.middlewares import setup_middlewares


def create_application() -> FastAPI:
    application = FastAPI(openapi_url='/api/openapi.json',
                          docs_url='/api/docs',
                          redoc_url='/api/redoc')
    application.include_router(api_router, prefix='/api', tags=['API'])

    register_all_exception_handlers(application)
    setup_middlewares(application)

    return application


app = create_application()


@app.get('/')
async def root(token: str = Query(...)) -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            'ping': 'pong'
                        })


register_tortoise(app,
                  db_url=get_database_settings().API_DATABASE_URI,
                  modules={
                      'models': ['app.orm.game']
                  },
                  generate_schemas=True,
                  add_exception_handlers=True)
