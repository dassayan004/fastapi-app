from typing import Annotated, List
from fastapi import APIRouter, Depends


from auth.auth_gurd import JWTBearer
from auth.schemas import (
    UserLogin,
    UserLoginResponse,
    UserRegister,
    UserRegisterResponse,
    UserResponse,
)
from auth.services import (
    authenticate_user,
    get_all_users,
    get_authenticated_user,
    register_user,
)
from database.dbSession import SessionDep


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/allUsers", summary="Get all users", response_model=List[UserResponse])
async def getAllUser(session: SessionDep):
    return await get_all_users(session)


@router.post(
    "/register",
    summary="Perform a User Registration",
    response_model=UserRegisterResponse,
)
async def register(user: UserRegister, session: SessionDep):
    return await register_user(user, session)


@router.post("/login", summary="Perform a User Login", response_model=UserLoginResponse)
async def login(user_data: UserLogin, db: SessionDep):
    return await authenticate_user(user_data, db)


@router.get(
    "/me",
    summary="Get current user",
    dependencies=[Depends(JWTBearer())],
    response_model=UserResponse,
)
async def me(token: Annotated[str, Depends(JWTBearer())], db: SessionDep):
    return await get_authenticated_user(token, db)
