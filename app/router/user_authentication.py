from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from schemas.user_auth_schema import (
    UserRegisterSchema,
    UserLogin
)
from utils.auth_utils import (
    get_password_hash,
    verify_password,
    authenticate_user,
    create_access_token
)

from bson import ObjectId
from db import db_dependency

router = APIRouter(
    prefix="/user-auth",
    tags=["user-auth"]
)

@router.post("/register", response_model=None)
async def register_user(user: UserRegisterSchema):
    user_in_db = db_dependency.users.find_one({"email": user.email})
    if user_in_db:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "User already exists"}
        )
        
    user.password = get_password_hash(user.password)
    _ = db_dependency.users.insert_one(user.model_dump())
    user_info = db_dependency.users.find_one({"email": user.email})
    
    # print(user_info)
    return JSONResponse({
        'message': 'User registered successfully',
        'data' : {
            'id' : str(user_info['_id']),
            'full_name': user_info['full_name'],
            'email': user_info['email']
            }
        }
    )
    
    
@router.post("/login", response_model=None)
async def login_user(user : UserLogin):
    user_info = authenticate_user(user.email, user.password)
    if user_info:
        access_token = create_access_token(data={
            'sub': str(user_info['_id']),
            'email': user_info['email']
        })
        return JSONResponse(
            access_token,
            status_code=status.HTTP_200_OK        
        )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Invalid credentials"}
    )
    
