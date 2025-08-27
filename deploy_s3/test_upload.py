# test_upload.py
import os, boto3
from dotenv import load_dotenv

load_dotenv()  # loads .env in the cwd

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

bucket = os.getenv("AWS_S3_BUCKET")
key = "healthchecks/hello.txt"
s3.put_object(Bucket=bucket, Key=key, Body=b"hello from RiceAI")
print(f"✅ uploaded to s3://{bucket}/{key}")
