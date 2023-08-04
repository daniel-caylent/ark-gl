import urllib.request
import ssl
import json
from urllib.parse import urlparse


def download_from_s3(signed_s3_url: str) -> str:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    response = urllib.request.urlopen(signed_s3_url, context=ctx, timeout=15)
    data = response.read()

    response.close()
    return data.decode("utf-8")


def save_to_s3(client, objects: [], bucket_name: str, prefix: str, index: str):
    filename = f"{prefix}_{index}.json"
    s3_path = f"{prefix}/{filename}"
    obj_json = json.dumps(objects, default=str)
    client.put_object(Bucket=bucket_name, Key=s3_path, Body=obj_json)
    return f"s3://{bucket_name}/{s3_path}"


def __get_bucket_and_file_key_from_path(file_path: str):
    parsed_url = urlparse(file_path)
    bucket_name = parsed_url.netloc
    return bucket_name, parsed_url.path.lstrip('/')


def load_from_s3(client, file_path: str):
    bucket_name, file_key = __get_bucket_and_file_key_from_path(file_path)
    file_obj = client.get_object(Bucket=bucket_name, Key=file_key)
    file_content = file_obj['Body'].read().decode('utf-8')
    return json.loads(file_content)


def delete_from_s3(client, file_path: str):
    bucket_name, file_key = __get_bucket_and_file_key_from_path(file_path)
    client.delete_object(Bucket=bucket_name, Key=file_key)
