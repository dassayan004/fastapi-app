from typing import List
from jwt import PyJWTError as JWTError
from models.userModels import User
from database.dbSession import SessionDep
from fastapi import HTTPException, Request, status
from sqlmodel import select
from auth.dependencies import decode_jwt, get_password_hash, sign_jwt, verify_password
from auth.schemas import (
    UserLogin,
    UserLoginResponse,
    UserRegister,
    UserRegisterResponse,
    UserResponse,
)
from sqlalchemy.exc import SQLAlchemyError


async def get_user_by_email(email: str, db: SessionDep) -> User:
    """Fetch a user by email from the database."""
    statement = select(User).where(User.email == email)
    result = await db.exec(statement)
    user = result.first()
    return user


async def get_all_users(db: SessionDep) -> List[UserResponse]:
    """Fetch all users from the database."""
    statement = select(User)
    result = await db.exec(statement)
    users = result.all()
    return [UserResponse.model_validate(user) for user in users]


async def get_user_by_id(id: str, db: SessionDep) -> User:
    """Fetch a user by id from the database."""
    statement = select(User).where(User.id == id)
    result = await db.exec(statement)
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


async def register_user(
    user_data: UserRegister,
    db: SessionDep,
) -> UserRegisterResponse:
    """Registers a new user"""

    try:
        if await get_user_by_email(user_data.email, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        new_user = User(
            email=user_data.email, password=get_password_hash(user_data.password)
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return UserRegisterResponse(user=new_user.model_dump())

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        ) from e


async def authenticate_user(user_data: UserLogin, db: SessionDep) -> UserLoginResponse:
    try:
        user = await get_user_by_email(user_data.email, db)
        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = sign_jwt(user_sub=str(user.id), user_email=user.email)

        return UserLoginResponse(access_token=access_token, user=user.model_dump())

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        ) from e


async def get_authenticated_user(token: str, db: SessionDep) -> UserResponse:
    try:
        payload = decode_jwt(token)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid or expired token")

        user_email = payload.get("email")
        user = await get_user_by_email(user_email, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**user.model_dump())

    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error") from e
