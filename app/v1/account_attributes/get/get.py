"""Lambda that will perform GET requests for AccountAttributes"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import account_attributes
from shared import endpoint
from models import Attribute
# pylint: enable=import-error


@endpoint
def handler(event, context): # pylint: disable=unused-argument; Required lambda parameters
    response = account_attributes.select_all()
    attributes = [Attribute(**attr) for attr in response]

    return 200, {"data": attributes}
