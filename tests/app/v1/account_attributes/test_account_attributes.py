import json

from tests.app.data import LambdaContext

from .account_attribute_test_base import AccountAttributeTestBase

class TestAccountAttributes(AccountAttributeTestBase):
    def test_get(self):
        from app.v1.account_attributes.get.get import handler
        result = handler({}, LambdaContext())
        assert 200 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.account_attributes.get.get import handler
        result = handler({}, LambdaContext())
        json.dumps(result)