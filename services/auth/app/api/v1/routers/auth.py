from app.orm.user import user_pydantic_out
from app.schemas.auth import AuthSchema, RegistrationSchema
from app.settings.config import (get_admin_infinity_token_settings,
                                 get_admin_settings)
from app.utils.auth import authenticate_user, register_user
from app.utils.decorators import login_required
from app.utils.user import (get_user_by_email, update_user_to_admin,
                            verify_admin)
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Path, Query
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

router = APIRouter()


@router.post('/registration')
async def registration(registration_data: RegistrationSchema) -> JSONResponse:
    user = await register_user(registration_data.email, registration_data.password)
    user_pydantic = await user_pydantic_out.from_tortoise_orm(user)

    return JSONResponse(status_code=200,
                        content={
                            'detail': {
                                'user': user_pydantic.dict()
                            }
                        })


@router.post('/login/user')
async def login(auth_data: AuthSchema, authorize: AuthJWT = Depends()) -> JSONResponse:
    user = await authenticate_user(auth_data)

    access_token = authorize.create_access_token(subject=user.email)

    return JSONResponse(status_code=200,
                        content={
                            'detail': {
                                'access_token': access_token
                            }
                        })


@router.get('/current')
@login_required(target='authorize', attribute='jwt_required')
async def current(authorize: AuthJWT = Depends()) -> JSONResponse:
    current_user = authorize.get_jwt_subject()
    user = await get_user_by_email(email=current_user)
    user_pydantic = await user_pydantic_out.from_tortoise_orm(user)

    return JSONResponse(status_code=200,
                        content={
                            'detail': {
                                'user': user_pydantic.dict()
                            }
                        })


@router.post('/update/permissions/{email}')
async def update_permissions(token: str = Query(...), email: str = Path(...)) -> JSONResponse:
    if not await verify_admin(token=token):
        raise HTTPException(status_code=403,
                            detail='invalid token passed')

    user = await get_user_by_email(email=email)
    await update_user_to_admin(user=user)

    return JSONResponse(status_code=200,
                        content={
                            'detail': {
                                'user': {
                                    'email': email,
                                    'is_admin': True
                                }
                            }
                        })


@router.post('/admin')
async def admin(token: str = Query(...)) -> JSONResponse:
    if not await verify_admin(token=token):
        raise HTTPException(status_code=403,
                            detail='invalid token passed')

    return JSONResponse(status_code=200,
                        content={
                            'detail': {
                                'user': {
                                    'id': 0,
                                    'email': get_admin_settings().ADMIN_LOGIN,
                                    'is_admin': True
                                }
                            }
                        })
