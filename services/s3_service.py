import boto3
import os
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def download_file_from_s3(s3_key):
    """Downloads a file from S3 and returns its content as bytes."""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
        return response['Body'].read()
    except ClientError as e:
        # Handle errors like file not found, permission issues, etc.
        print(f"Error downloading file {s3_key} from S3: {e}")
        return None

def generate_presigned_url(s3_key, expiration=3600):
    """Generates a presigned URL for a file in S3."""
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        print(f"Error generating presigned URL for {s3_key}: {e}")
        return None