import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

from dotenv import load_dotenv

load_dotenv()

# Load from environment (your .env must be sourced or use dotenv)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "eu-north-1")
BUCKET_NAME = os.getenv("AWS_S3_BUCKET", "riceai-chatstore")


def check_s3_connection():
    try:
        # Initialize client
        s3 = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        # Try listing objects (just first 5)
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=5)

        print(f"✅ Connected to bucket: {BUCKET_NAME} in {AWS_REGION}")
        if "Contents" in response:
            print("Objects found:")
            for obj in response["Contents"]:
                print(" -", obj["Key"])
        else:
            print("Bucket is empty (but connection is good).")

    except NoCredentialsError:
        print("❌ No credentials found. Check your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
    except ClientError as e:
        print("❌ AWS Client error:", e)
    except Exception as e:
        print("❌ Unexpected error:", e)


if __name__ == "__main__":
    check_s3_connection()
