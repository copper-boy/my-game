from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.orm.user import user_pydantic_out
from app.schemas.auth import AuthSchema, RegistrationSchema
from app.utils.auth import authenticate_user, register_user
from app.utils.decorators import login_required
from app.utils.user import get_user_by_email

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


@router.post('/login')
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
