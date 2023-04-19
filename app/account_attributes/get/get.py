from shared import endpoint

from models import Attribute

@endpoint
def handler(event, context):
    #response = db.get_account_attributes()
    response = [
        {
            'attributeNo': 1,
            'accountType': "Assets",
            'detailType': "Balance Sheet"
        },
        {
            'attributeNo': 2,
            'accountType': "Assets",
            'detailType': "Balance Sheet"
        }
    ]

    attributes = [Attribute(**attr) for attr in response]

    return 200, {'data': attributes}
