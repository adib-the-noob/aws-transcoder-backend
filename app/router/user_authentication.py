from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

from schemas.user_auth_schema import (
    UserRegisterSchema,
    UserLogin,
    UserInDb
)
from utils.auth_utils import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user
)
from models.auth_models import User

from db import db_dependency

router = APIRouter(
    prefix="/user-auth",
    tags=["user-auth"]
)

@router.post("/register", response_model=None)
async def register_user(
    user: UserRegisterSchema,
    db : db_dependency
):
    email = db.query(User).filter(User.email == user.email).first()
    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=get_password_hash(user.password)
    )
    new_user.save(db)
    return JSONResponse({
        "id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name
    }, status_code=status.HTTP_201_CREATED)


@router.get("/me", response_model=None)
async def get_me(db : db_dependency, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user['sub']).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return JSONResponse({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }, status_code=status.HTTP_200_OK)
    
    
@router.post("/token", response_model=None)
async def get_token(
    db : db_dependency,
    form_data : Annotated[OAuth2PasswordRequestForm, None] = Depends()
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={
        'sub': user.id,
        'email': user.email
    })
    return JSONResponse(
        access_token,
        status_code=status.HTTP_200_OK
    )