from fastapi.background import BackgroundTasks
from fastapi import UploadFile

from models.video_models import Video
from db import db_dependency
from schemas.video_schema import UploadVideoModel
from aws.s3_uploader import (
    s3_client,
    BUCKET_NAME
)

def upload_part_to_s3(bucket_name, key, upload_id, part_number, chunk):
    try:
        response = s3_client.upload_part(
            Bucket=bucket_name,
            Key=key,
            PartNumber=part_number,
            UploadId=upload_id,
            Body=chunk
        )
        return {
            'PartNumber': part_number,
            'ETag': response['ETag']
        }
    except Exception as e:
        return {"error": str(e)}