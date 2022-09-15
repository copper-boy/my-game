from logging import getLogger

from pydantic import EmailStr

from app.orm.user import UserModel
from app.settings.config import get_admin_infinity_token_settings

logger = getLogger('user')


async def get_user_by_email(email: EmailStr) -> UserModel:
    user = await UserModel.get(email=email)

    return user


async def update_user_to_admin(user: UserModel) -> None:
    await user.update_from_dict({
            'is_admin': True
    })
    await user.save()


async def verify_admin(token: str) -> bool:
    config = get_admin_infinity_token_settings()

    return token == config.INFINITY_ADMIN_TOKEN
