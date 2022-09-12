from fastapi import FastAPI
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

from app.api import api_router
from app.settings.config import get_database_settings
from app.settings.handlers import register_all_exception_handlers
from app.settings.middlewares import setup_middlewares


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router, prefix='/api')

    register_all_exception_handlers(application)
    setup_middlewares(application)

    return application


app = create_application()


@app.get('/')
async def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            'ping': 'pong'
                        })


register_tortoise(app,
                  db_url=get_database_settings().LOGIC_DATABASE_URI,
                  modules={
                      'models': ['app.orm.game', 'app.orm.session']
                  },
                  generate_schemas=True,
                  add_exception_handlers=True)
