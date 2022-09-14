from asyncio import sleep
from logging import getLogger

from fastapi.exceptions import HTTPException
from pydantic import EmailStr

from app.orm.user import UserModel
from app.schemas.auth import AuthSchema
from app.settings.config import get_admin_settings
from app.utils.auth import authenticate_user, register_user

logger = getLogger('user')


async def get_user_by_email(email: EmailStr) -> UserModel:
    user = await UserModel.get(email=email)

    return user


async def update_user_to_admin(user: UserModel) -> None:
    await user.update_from_dict({
            'is_admin': True
    })
    await user.save()


async def __setup_admin() -> None:
    config = get_admin_settings()
    try:
        user = await register_user(config.ADMIN_LOGIN,
                                   config.ADMIN_PASSWORD)
    except HTTPException:
        user = await authenticate_user(AuthSchema(email=config.ADMIN_LOGIN,
                                                  password=config.ADMIN_PASSWORD))
    await update_user_to_admin(user)


async def register_admin() -> None:
    config = get_admin_settings()
    try:
        user = await register_user(config.ADMIN_LOGIN,
                                   config.ADMIN_PASSWORD)
    except HTTPException:
        user = await authenticate_user(AuthSchema(email=config.ADMIN_LOGIN,
                                                  password=config.ADMIN_PASSWORD))
    await update_user_to_admin(user)
