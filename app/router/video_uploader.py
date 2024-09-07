import uuid

from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi.responses import JSONResponse

from db import db_dependency, get_db_dependency
from utils.auth_utils import get_current_user
from aws.s3_uploader import s3_client

from schemas.video_schema import UploadVideoModel
from bson import ObjectId 


router = APIRouter(
    prefix="/videos",
    tags=["videos"]
)

AWS_BUCKET_NAME = 'transcoder-raw-bucket'

@router.post("/upload-video", response_model=None)
async def upload_video_on_s3(
    video: UploadVideoModel = Depends(),
    user: dict = Depends(get_current_user),
    db_dependency = Depends(get_db_dependency),
):
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )
    
    channel_info = db_dependency.channels.find({"_id": video.channel_id, "owner_id": user['sub']})
  
    if channel_info is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid channel"}
        )
    
    file_uuid = str(uuid.uuid4())
    video_info = {
        "video_uuid": file_uuid,
        "title": video.title,
        "description": video.description,
        "channel_id": video.channel_id,
        "visibility": video.visibility,
        "owner_id": user['sub']
    }
    db_dependency.videos.insert_one(video_info)
    
    try:
        file = video.video_file
        file_name = f"{file_uuid}__{file.filename}"
        response = s3_client.create_multipart_upload(
            Bucket=AWS_BUCKET_NAME,
            Key=file_name,
            ContentType=file.content_type
        )

        upload_id = response['UploadId']
        
        parts = []
        part_number = 1
        chunk_size = 5 * 1024 * 1024
        
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            part = s3_client.upload_part(
                Bucket=AWS_BUCKET_NAME,
                Key=file_name,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=chunk
            )
            parts.append({
                'PartNumber': part_number,
                'ETag': part['ETag'] # Etage is a unique identifier for the part
            })
            part_number += 1    
            
        s3_client.complete_multipart_upload(
            Bucket=AWS_BUCKET_NAME,
            Key=file_name,
            UploadId=upload_id,
            MultipartUpload={
                'Parts': parts
            }
        )
        
        # video data update
        update_query = {
            "video_uuid": file_uuid
        }
        
        updated_data = {
            "$set": {
                "upload_status": "uploaded",
                "raw_video": {
                    "file_name": file_name,
                    "key": file_name,
                    "s3_url": f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{file_name}",
                    "content_type": file.content_type,
                }                    
            }
        }
        
        db_dependency = db_dependency.videos.update_one(update_query, updated_data)
        
        video_info.update({
            'file_name': file_name,
            "s3_url": f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        })
        
        return {
            "message": "Video uploaded successfully",
            "filename": file.filename,
            "url": f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "An error occured",
            "error": str(e)
        }
        
        
@router.get("/get-video-info/{video_uuid}", response_model=None)
def get_video_info(video_uuid: str):
    video_info = db_dependency.videos.find_one(
        {
            "video_uuid": video_uuid
        }
    )
   
    if not video_info:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Video not found"}
        )
            
    video_info['_id'] = str(video_info['_id'])
    video_info['channel_id'] = str(video_info['channel_id'])
    video_info['owner_id'] = str(video_info['owner_id'])
    
    return video_info


@router.get("/get-videos/{channel_id}", response_model=None)
async def get_videos(channel_id: str):
    videos = db_dependency.videos.find(
        {
            "channel_id": channel_id
        },
    )
    
    video_list = []
    for video in videos:
        video['_id'] = str(video['_id'])
        video['channel_id'] = str(video['channel_id'])
        video['owner_id'] = str(video['owner_id'])
        video_list.append(video)
    return video_list