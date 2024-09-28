import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from db import db_dependency
from utils.auth_utils import get_current_user
from aws.s3_uploader import s3_client

from schemas.video_schema import UploadVideoModel
from models.auth_models import User
from models.channel_models import Channel
from models.video_models import Video

router = APIRouter(
    prefix="/videos",
    tags=["videos"]
)

AWS_BUCKET_NAME = 'transcoder-raw-bucket'

@router.post("/upload-video", response_model=None)
async def upload_video_on_s3(
    db: db_dependency,
    video: UploadVideoModel = Depends(),
    user: dict = Depends(get_current_user),
):
    # Fetch the user from the database
    user = db.query(User).filter(User.id == user['sub']).first()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"}
        )
    
    # Generate a unique file UUID for the video file
    file_uuid = str(uuid.uuid4())

    # Fetch the user's channel information
    channel_info = db.query(Channel).filter(Channel.owner_id == user.id).first()
    if not channel_info:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Channel not found"}
        )

    try:
        # Get the uploaded file object and generate the S3 key (file name)
        file = video.video_file
        file_name = f"{file_uuid}__{file.filename}"
        
        # Initiate multipart upload to S3
        response = s3_client.create_multipart_upload(
            Bucket=AWS_BUCKET_NAME,
            Key=file_name,
            ContentType=file.content_type  # Use content type of uploaded file
        )
        upload_id = response['UploadId']
        
        parts = []
        part_number = 1
        chunk_size = 5 * 1024 * 1024  # 5 MB chunk size
        
        # Read and upload the file in chunks to S3
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break

            # Upload each part of the file
            part = s3_client.upload_part(
                Bucket=AWS_BUCKET_NAME,
                Key=file_name,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=chunk
            )
            parts.append({
                'PartNumber': part_number,
                'ETag': part['ETag']  # Store the ETag for each part
            })
            part_number += 1
        
        # Complete the multipart upload once all parts are uploaded
        s3_client.complete_multipart_upload(
            Bucket=AWS_BUCKET_NAME,
            Key=file_name,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        
        # Check if the video record exists in the database, update or create accordingly
        video_data = Video(
            video_uuid=file_uuid,
            title=video.title,
            description=video.description,
            visibility=video.visibility.value,
            channel_id=channel_info.id,
            s3_key=file_name,
            bucket_name=AWS_BUCKET_NAME,
        )
        video_data.save(db)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Video uploaded successfully"}
        )
        
    except Exception as e:
        # Handle any errors, including aborting the multipart upload if necessary
        if 'upload_id' in locals():
            s3_client.abort_multipart_upload(
                Bucket=AWS_BUCKET_NAME,
                Key=file_name,
                UploadId=upload_id
            )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An error occurred during upload", "error": str(e)}
        )