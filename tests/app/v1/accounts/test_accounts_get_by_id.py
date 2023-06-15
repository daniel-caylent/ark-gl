import json

from tests.app.data import (
    LambdaContext
)

from .accounts_test_base import AccountsTestBase

class TestAccountsGetById(AccountsTestBase):

    def test_good_api_request(self):
        request = {
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
            }
        }
        from app.v1.accounts.get.get_by_id import handler
        result = handler(request, LambdaContext())
        assert 200 == result['statusCode']

    def test_no_account_id(self):
        request = {
            "pathParameters": {
            }
        }
        from app.v1.accounts.get.get_by_id import handler
        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_bad_account_id(self):
        request = {
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df9"
            }
        }
        from app.v1.accounts.get.get_by_id import handler
        result = handler(request, LambdaContext())
        assert 404 == result['statusCode']

    def test_non_uui_id(self):
        request = {
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
            }
        }
        from app.v1.accounts.get.get_by_id import handler
        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_is_json_encodable(self):
        request = {
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
            }
        }
        from app.v1.accounts.get.get_by_id import handler
        result = handler(request, LambdaContext())
        json.dumps(result)