from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from orm.user import (AdminModel, UserModel, admin_pydantic_out,
                      user_pydantic_out)
from schemas.auth import AuthSchema, RegistrationSchema
from utils.auth import authenticate_user, register_user
from utils.decorators import login_required

router = APIRouter()


@router.post('/registration')
async def registration(registration_data: RegistrationSchema) -> JSONResponse:
    user = await register_user(registration_data.email, registration_data.password)

    if user is not None:
        raise HTTPException(status_code=400,
                            detail='cannot register new user')
    user_pydantic = await user_pydantic_out.from_tortoise_orm(user)

    return JSONResponse(status_code=200,
                        content={
                            'detail': {
                                'user': user_pydantic.__dict__
                            }
                        })


@router.post('/login')
async def login(auth_data: AuthSchema, authorize: AuthJWT = Depends()) -> JSONResponse:
    _unused = await authenticate_user(auth_data)

    access_token = authorize.create_access_token(subject=auth_data.email)

    return JSONResponse(status_code=200,
                        content={
                            'detail': {
                                'access_token': access_token
                            }
                        })


@router.post('/refresh')
@login_required(target='authorize', attribute='jwt_required')
async def refresh(authorize: AuthJWT = Depends()) -> JSONResponse:
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)

    return JSONResponse(status_code=200,
                        content={
                            'detail': {
                                'access_token': new_access_token
                            }
                        })


@router.get('/current')
@login_required(target='authorize', attribute='jwt_required')
async def current(authorize: AuthJWT = Depends()) -> JSONResponse:
    current_user = authorize.get_jwt_subject()

    user_object = await UserModel.get_or_none(email=current_user)
    admin_object = await AdminModel.get_or_none(user=user_object)

    user_pydantic = await user_pydantic_out.from_tortoise_orm(user_object)
    if admin_object is None:
        return JSONResponse(status_code=200,
                            content={
                                'detail': {
                                    'user': user_pydantic.__dict__
                                }
                            })

    admin_pydantic = await admin_pydantic_out.from_tortoise_orm(admin_object)
    return JSONResponse(status_code=200,
                        content={
                            'detail': {
                                'user': user_pydantic.__dict__,
                                'admin': admin_pydantic.__dict__
                            }
                        })
