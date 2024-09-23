import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from db import db_dependency
from utils.auth_utils import (
    get_current_user
)
from schemas.channel_schema import (
    CreateChannelModel,
)

from models.auth_models import User
from models.channel_models import Channel
from models.video_models import Video

router = APIRouter(
    prefix="/channels",
    tags=["channels"]
)

@router.post("/create", response_model=None)
async def create_channel(
    db : db_dependency,
    channel: CreateChannelModel,
    user: dict = Depends(get_current_user)
):
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "User not found"}
        )

    user = db.query(User).filter(
        User.email == user['email']
    ).first()
    
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "User not found"}
        )
    # insert channel
    created_channel = Channel(
        name=channel.name,
        description=channel.description,
        owner_id=user.id
    )
    created_channel.save(db)
    return JSONResponse({
        "status" : 'success',
        'data' : {
            "name" : created_channel.name,
            "desc" : created_channel.description
        }
    })
    
    
@router.get("/list-channels", response_model=None)
async def list_channels(
    db : db_dependency,
    user: dict = Depends(get_current_user)
):
    
    # load all channels
    channels = db.query(Channel).filter(
         Channel.owner_id == user['sub']
    ).all()
    data = []
    for channel in channels:
       data.append({
        "id" : channel.id,
        "name" : channel.name,
        "description" : channel.description
        })
    
    return JSONResponse({
        "status" : 'success',
        'data' : data
    })