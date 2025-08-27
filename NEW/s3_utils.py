# s3_utils.py
import os, mimetypes
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

_S3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_DEFAULT_REGION", "eu-west-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
_BUCKET = os.environ["S3_BUCKET_CHATS"]

def _norm_key(key: str) -> str:
    return key.lstrip("/")

def upload_file(local_path: str | Path, key: str) -> None:
    key = _norm_key(key)
    ct, _ = mimetypes.guess_type(str(local_path))
    extra = {"ContentType": ct} if ct else {}
    _S3.upload_file(str(local_path), _BUCKET, key, ExtraArgs=extra)

def download_file(key: str, local_path: str | Path) -> bool:
    key = _norm_key(key)
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    try:
        _S3.download_file(_BUCKET, key, str(local_path))
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] in ("404", "NoSuchKey"):
            return False
        raise

def list_keys(prefix: str) -> list[str]:
    prefix = _norm_key(prefix.rstrip("/") + "/")
    out, token = [], None
    while True:
        resp = _S3.list_objects_v2(Bucket=_BUCKET, Prefix=prefix, ContinuationToken=token) \
               if token else _S3.list_objects_v2(Bucket=_BUCKET, Prefix=prefix)
        for obj in resp.get("Contents", []):
            out.append(obj["Key"])
        token = resp.get("NextContinuationToken")
        if not token:
            break
    return out

def upload_dir(local_dir: str | Path, prefix: str) -> None:
    local_dir = Path(local_dir)
    for p in local_dir.rglob("*"):
        if p.is_file():
            rel = p.relative_to(local_dir)
            upload_file(p, f"{prefix.rstrip('/')}/{rel.as_posix()}")

def backup_sqlite(local_sqlite: str | Path, prefix_sqlite: str) -> None:
    name = Path(local_sqlite).name
    upload_file(local_sqlite, f"{prefix_sqlite.rstrip('/')}/{name}")
