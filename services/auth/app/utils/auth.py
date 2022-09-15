from app.orm.user import UserModel
from app.schemas.auth import AuthSchema
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr
from tortoise.exceptions import IncompleteInstanceError, IntegrityError

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify password with hashed password.

    :param: password: not encrypted password
    :param: hashed_password: encrypted password
    :return: True if hash and password did match else False
    """
    try:
        is_verified = pwd_context.verify(password, hashed_password)
        return is_verified
    except (ValueError, TypeError):
        return False


async def get_password_hash(password: str) -> str:
    """
    Returns the encrypted password based on the normal password.

    :param: password: not encrypted password
    :return: hashed password
    """
    hashed_password = pwd_context.hash(password)
    return hashed_password


async def authenticate_user(auth_data: AuthSchema) -> UserModel:
    user = await UserModel.get(email=auth_data.email)

    is_password_verified = await verify_password(auth_data.password, user.password)

    if not user or not is_password_verified:
        raise HTTPException(status_code=403,
                            detail='incorrect login data posted')
    return user


async def register_user(email: EmailStr, password: str) -> UserModel | None:
    try:
        exists_user = await UserModel.get_or_none(email=email)
        if exists_user is None:
            hashed_password = await get_password_hash(password)

            user = await UserModel.create(email=email,
                                          password=hashed_password)
        else:
            raise HTTPException(status_code=409,
                                detail='current user exists')
    except (IncompleteInstanceError, IntegrityError):
        user = await UserModel.get(email=email)
        await user.delete()
    else:
        return user


async def delete_user(email: EmailStr) -> None:
    user = await UserModel.get_or_none(email=email)

    if user is not None:
        await user.delete()
