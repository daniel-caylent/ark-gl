import boto3

from arkdb import account_attributes    # pylint: disable=import-error
from shared import endpoint             # pylint: disable=import-error
from models import Attribute            # pylint: disable=import-error

@endpoint
def handler(event, context):
    response = account_attributes.select_all()
    attributes = [Attribute(**attr) for attr in response]

    return 200, {'data': attributes}
