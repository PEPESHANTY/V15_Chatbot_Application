# test_delete.py
import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load env
load_dotenv()

AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
BUCKET = os.getenv("AWS_S3_BUCKET")
KEY = "healthchecks/hello.txt"   # same file we uploaded earlier

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

try:
    s3.delete_object(Bucket=BUCKET, Key=KEY)
    print(f"🗑️ Deleted s3://{BUCKET}/{KEY}")
except ClientError as e:
    print("❌ Error deleting:", e)
