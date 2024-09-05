import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from db import db_dependency
from utils.auth_utils import (
    get_current_user
)
from schemas.channel_schema import (
    CreateChannelModel,
    ChannelModel
)

router = APIRouter(
    prefix="/channels",
    tags=["channels"]
)

@router.post("/create", response_model=ChannelModel)
async def create_channel(
    channel: CreateChannelModel,
    current_user: dict = Depends(get_current_user)
):
    user = db_dependency.users.find_one({"email": current_user['email']})
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "User not found"}
        )

    channel.owner_id = str(user['_id'])
    _ = db_dependency.channels.insert_one({
        **channel.model_dump(),
        'id': str(uuid.uuid4()),
        'owner_id': str(user['_id'])
    })
    channel_info = db_dependency.channels.find_one({"name": channel.name})
    
    return JSONResponse({
        'message': 'Channel created successfully',
        'data' : {
            'id' : str(channel_info['_id']),
            'name': channel_info['name'],
            'description': channel_info['description']
            }
        }
    )


@router.get("/list-channels", response_model=ChannelModel)
async def list_channels(
    user: dict = Depends(get_current_user)
):
    channels = db_dependency.channels.find({"owner_id": str(user['sub'])})
    channel_list = []
    for channel in channels:
        channel_list.append({
            'id': str(channel['_id']),
            'name': channel['name'],
            'description': channel['description']
        })
    return JSONResponse({
        'message': 'Channels fetched successfully',
        'data': channel_list
    })
    
    