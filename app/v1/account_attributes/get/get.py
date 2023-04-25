import boto3

from arkdb import account_attributes
from shared import endpoint
from .models import Attribute

@endpoint
def handler(event, context):
    response = account_attributes.get_all()
    attributes = [Attribute(**attr) for attr in response]

    return 200, {'data': attributes}
