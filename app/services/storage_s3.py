import boto3, hashlib, os
s3 = boto3.client("s3")
BUCKET = os.getenv("S3_BUCKET","")
def put_bytes(key:str, b:bytes) -> tuple[str,str]:
    if not BUCKET:
        raise RuntimeError("S3_BUCKET not configured")
    checksum = hashlib.sha256(b).hexdigest()
    s3.put_object(Bucket=BUCKET, Key=key, Body=b)
    return key, checksum
