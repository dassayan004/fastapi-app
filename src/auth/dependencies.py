from typing import Dict
from argon2 import PasswordHasher
import jwt
from pydantic import BaseModel


from core.config import appSetting

ph = PasswordHasher()


def get_password_hash(password: str) -> str:
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except:
        return False


class JWTSettings(BaseModel):
    authjwt_secret_key: str = appSetting.SECRET_KEY
    authjwt_algorithm: str = appSetting.JWT_ALGORITHM
    expires_in: int = appSetting.ACCESS_TOKEN_EXPIRE_MINUTES


jwtSettings = JWTSettings()


def sign_jwt(user_sub: str, user_email: str) -> Dict[str, str]:
    payload = {
        "sub": user_sub,
        "email": user_email,
        "expires": jwtSettings.expires_in
    }
    token = jwt.encode(payload, jwtSettings.authjwt_secret_key,
                       algorithm=jwtSettings.authjwt_algorithm)

    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, jwtSettings.authjwt_secret_key, algorithms=[
            jwtSettings.authjwt_algorithm])
        return decoded_token if decoded_token["expires"] >= jwtSettings.expires_in else None
    except:
        return {}
