import json

from tests.app.data import (
    LambdaContext
)

from .accounts_test_base import AccountsTestBase

class TestAccountsDelete(AccountsTestBase):

    def test_good_api_request(self):
        from app.v1.accounts.delete.bulk import handler
        request = {
            "body": json.dumps({
                "accountIds": ["a92bde1e-7825-429d-aaae-909f2d7a8df1"]
            })
        }
        result = handler(request, LambdaContext())

        print(result)
        assert 200 == result['statusCode']

    def test_bad_id_request(self):
        from app.v1.accounts.delete.bulk import handler
        request = {
            "body": json.dumps({
                "accountIds": ["a92bde1e-7825-429d-aaae-909f2d7a8df"]
            })
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_missing_id(self):
        from app.v1.accounts.delete.bulk import handler
        request = {
            "body": json.dumps({
                "accountIds": []
            })
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_missing_body(self):
        from app.v1.accounts.delete.bulk import handler
        request = {
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_delete_posted(self):
        from app.v1.accounts.delete.bulk import handler
        request = {
            "queryStringParameters": json.dumps({
                "accountIds": ["a92bde1e-7825-429d-aaae-909f2d7a8df5"]
            })
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']
