import json

from tests.app.data import (
    LambdaContext
)

from .accounts_test_base import AccountsTestBase

class TestAccountsDelete(AccountsTestBase):

    def test_good_api_request(self):
        from app.v1.accounts.delete.delete import handler
        request = {
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }
        result = handler(request, LambdaContext())
        assert 200 == result['statusCode']

    def test_bad_id_request(self):
        from app.v1.accounts.delete.delete import handler
        request = {
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8d"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_missing_id(self):
        from app.v1.accounts.delete.delete import handler
        request = {
            "pathParameters": {
                "accountId": None
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_missing_path_params(self):
        from app.v1.accounts.delete.delete import handler
        request = {
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_delete_posted(self):
        from app.v1.accounts.delete.delete import handler
        request = {
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']
