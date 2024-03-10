from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt, JWTError
from pydantic import EmailStr, BaseSettings
from typing import Optional

class Settings(BaseSettings):
    SECRETE_KEY: str
    class Config:
        env_file = ".env"


settings = Settings()

#토큰 생성
def create_access_token(user: EmailStr, exp: int):
    payload = {
        "user": user,
        "exp": exp
    }
    token = jwt.encode(payload, settings.SECRETE_KEY, algorithm="HS256")
    return token

#토큰 검증
def verify_access_token(token: str):
    try:
        data = jwt.decode(token, settings.SECRETE_KEY, algorithms=["HS256"])
        expires = data.get("exp")
        if expires is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="No access token supplied")
        if datetime.utcnow() > datetime.utcfromtimestamp(expires):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Token is expired")
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token")