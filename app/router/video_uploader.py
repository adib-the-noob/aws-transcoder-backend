import os
import uuid

from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi.responses import JSONResponse

from db import db_dependency
from utils.auth_utils import get_current_user
from aws.s3_uploader import s3_client

from schemas.video_schema import UploadVideoModel

router = APIRouter(
    prefix="/videos",
    tags=["videos"]
)


@router.post("/upload-video", response_model=None)
async def upload_video_on_s3(
    video: UploadVideoModel = Depends(),
    # file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )
    
    channel_info = db_dependency.channels.find({"_id": video.channel_id, "owner_id": user['sub']})
  
    if not channel_info:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid channel"}
        )
        
    video_info = {
        "title": video.title,
        "description": video.description,
        "channel_id": video.channel_id,
        "visibility": video.visibility,
        "owner_id": user['sub']
    }
    db_dependency.videos.insert_one(video_info)
    
    try:
        file = video.video_file
        file_name = f"{uuid.uuid4()}__{file.filename}"
        response = s3_client.create_multipart_upload(
            Bucket='transcoder-raw-bucket',
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
                Bucket='transcoder-raw-bucket',
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
            Bucket='transcoder-raw-bucket',
            Key=file_name,
            UploadId=upload_id,
            MultipartUpload={
                'Parts': parts
            }
        )
        
        video_info.update({
            'file_name': file_name,
            "s3_url": f"https://transcoder-raw-bucket.s3.amazonaws.com/{file_name}"
        })
        
        return {
            "message": "Video uploaded successfully",
            "filename": file.filename,
            "url": f"https://transcoder-raw-bucket.s3.amazonaws.com/{file.filename}"
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "An error occured",
            "error": str(e)
        }