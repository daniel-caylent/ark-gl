import urllib.request
import ssl

def download_from_s3(signed_s3_url: str) -> str:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    response = urllib.request.urlopen(signed_s3_url, context=ctx)
    data = response.read()
    return data.decode("utf-8")

