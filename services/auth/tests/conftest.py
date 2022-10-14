import pytest
from aiohttp.test_utils import loop_context
from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
from tortoise import Tortoise

from app.main import app
from app.schemas.auth import AuthSchema
from app.utils.auth import authenticate_user, register_user

AUTH_SITE_URL = 'http://auth_service:8956'
DB_URI = 'sqlite://:memory:'


@pytest.fixture(scope='session')
def event_loop():
    with loop_context() as _loop:
        yield _loop


async def init_db(db_url: str) -> None:
    await Tortoise.init(
        db_url=db_url,
        modules={
            'models': ['app.orm.user']
        },
        _create_db=False
    )
    await Tortoise.generate_schemas()


async def init():
    await init_db(DB_URI)


@pytest.fixture(scope='session', autouse=True)
async def init_tests():
    await init()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session')
def server() -> FastAPI:
    yield app


@pytest.fixture(scope='session')
async def cli(server):
    async with AsyncClient(app=app, base_url=AUTH_SITE_URL) as client:
        yield client


@pytest.fixture(scope='session')
async def authed_cli(cli, default_user):
    resp = await cli.post(url='/api/v1/auth/login',
                          json={
                              'email': 'some@email.com',
                              'password': 'very_strong_password'
                          })
    resp_json = resp.json()
    cli.headers['Authorization'] = f'Bearer {resp_json["detail"]["access_token"]}'

    yield cli


@pytest.fixture(scope='session')
async def default_user():
    try:
        user = await register_user('some@email.com', 'very_strong_password')
    except HTTPException:
        user = await authenticate_user(AuthSchema(email='some@email.com',
                                                  password='very_strong_password'))
    yield user
