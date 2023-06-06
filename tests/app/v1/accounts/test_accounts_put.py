import pytest

from tests.app.data import (
    LambdaContext
)

from .accounts_test_base import AccountsTestBase

class TestAccountsPut(AccountsTestBase):

    def test_good_put(self):
        from app.v1.accounts.put.put import handler
        request = {
            "body": "{\"accountNo\": 101,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            },
        }

        result = handler(request, LambdaContext())
        assert 200 == result['statusCode']

    def test_put_with_parent_id(self):
        from app.v1.accounts.put.put import handler
        request = {
            "body": "{\"accountNo\": 101,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            },
        }

        result = handler(request, LambdaContext())
        assert 200 == result['statusCode']

    def test_put_with_bad_uuid(self):
        from app.v1.accounts.put.put import handler
        request = {
            "body": "{\"accountNo\": 101,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
            },
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_put_with_posted_account(self):
        from app.v1.accounts.put.put import handler
        request = {
            "body": "{\"accountNo\": 101,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
            },
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_put_with_posted_account_allowed(self):
        from app.v1.accounts.put.put import handler
        request = {
            "body": "{\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"}",
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
            },
        }

        result = handler(request, LambdaContext())
        assert 200 == result['statusCode']

    def test_put_with_bad_body(self):
        from app.v1.accounts.put.put import handler
        request = {
            "body": "{\"fsName\": \"fsName\",: \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"}",
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
            },
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_put_with_duplicate_name(self):
        from app.v1.accounts.put.put import handler
        request = {
            "body": "{\"accountNo\": 101,\"accountName\": \"account name\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            },
        }

        result = handler(request, LambdaContext())
        assert 409 == result['statusCode']

    def test_put_with_duplicate_account_number(self):
        from app.v1.accounts.put.put import handler
        request = {
            "body": "{\"accountNo\": 5555,\"accountName\": \"duplicate\", \"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
            "pathParameters": {
                "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            },
        }

        result = handler(request, LambdaContext())
        assert 409 == result['statusCode']