import os
import uuid

import boto3
from botocore.exceptions import ClientError

S3_ENDPOINT_URL = os.environ["S3_ENDPOINT_URL"]
S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

_s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)


def ensure_bucket_exists() -> None:
    """Create the target bucket on startup if it doesn't already exist."""
    try:
        _s3_client.head_bucket(Bucket=S3_BUCKET_NAME)
    except ClientError:
        _s3_client.create_bucket(Bucket=S3_BUCKET_NAME)


def upload_file(file_obj, content_type: str) -> str:
    """Upload a file-like object and return the object key it was stored under."""
    object_key = f"{uuid.uuid4()}"
    _s3_client.upload_fileobj(
        file_obj,
        S3_BUCKET_NAME,
        object_key,
        ExtraArgs={"ContentType": content_type},
    )
    return object_key


def download_file(object_key: str):
    """Return a streaming body for the stored object."""
    response = _s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=object_key)
    return response["Body"]


def delete_file(object_key: str) -> None:
    _s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=object_key)
