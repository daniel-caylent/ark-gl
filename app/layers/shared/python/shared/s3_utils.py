import urllib.request
import ssl
import json


def download_from_s3(signed_s3_url: str) -> str:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    response = urllib.request.urlopen(signed_s3_url, context=ctx)
    data = response.read()
    return data.decode("utf-8")


def save_to_s3(client, objects: [], bucket_name: str, prefix: str):
    s3_filenames = []
    for index, obj in enumerate(objects):
        filename = f"{prefix}_{index}.json"
        s3_path = f"{prefix}/{filename}"

        obj_json = json.dumps(obj)

        client.put_object(Bucket=bucket_name, Key=s3_path, Body=obj_json)

        s3_filenames.append(f"s3://{bucket_name}/{s3_path}")

    return s3_filenames
