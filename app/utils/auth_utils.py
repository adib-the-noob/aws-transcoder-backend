from db import db_dependency
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str):
    user = db_dependency.users.find_one({"email": email})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


# jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from datetime import datetime, timedelta, timezone
from jwt import PyJWTError, decode, encode
from config import base_config

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> dict:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=120)
    to_encode.update({"exp": expire})
    
    encoded_jwt = encode(
        to_encode, base_config.SECRET_KEY, algorithm=base_config.ALGORITHM
    )
    
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer"
    }
    
def decode_access_token(token: str):
    try:
        payload = decode(token, base_config.SECRET_KEY, algorithms=[base_config.ALGORITHM])
        return payload
    except PyJWTError:
        return None
    
    
def get_current_user(
    token: Annotated[str, OAuth2PasswordBearer(tokenUrl="/user-auth/login")]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    return payload