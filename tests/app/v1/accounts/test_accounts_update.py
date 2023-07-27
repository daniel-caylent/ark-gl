import json
from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.utils import APP_DIR

from .accounts_test_base import getAccountsBase
put_dir = str(PurePath(APP_DIR, 'accounts', 'put'))

class TestAccountsUpdate(getAccountsBase([put_dir])):

    def test_good_put(self):
        from app.v1.accounts.put.update import handler

        body = {
            "accounts": [
                {
                    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                    "accountNo": 101,
                    "accountName": "unique",
                    "accountDescription": "account description",
                    "isTaxable": True,
                    "isEntityRequired": False,
                    "parentAccountId": None,
                    "attributeId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                    "fsName": "fsName",
                    "fsMappingId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                }
            ]
        }
        
        request = {
            "body": json.dumps(body)
        }

        result = handler(request,
        LambdaContext())

        assert 200 == result['statusCode']


    def test_bad_body(self):
        from app.v1.accounts.put.update import handler
        
        request = {
            "body": "{\"THIS IS NOT JSON\"}"
        }

        result = handler(request,
        LambdaContext())
        assert 400 == result['statusCode']

    def test_empty_accounts(self):
        from app.v1.accounts.put.update import handler

        body = {
            "accounts": []
        }
        
        request = {
            "body": json.dumps(body)
        }

        result = handler(request,
        LambdaContext())

        assert 400 == result['statusCode']

    def test_good_put(self):
        from app.v1.accounts.put.update import handler

        body = {
            "accounts": [
                {
                    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                    "accountNo": 101,
                    "accountName": "unique",
                    "accountDescription": "account description",
                    "isTaxable": True,
                    "isEntityRequired": False,
                    "parentAccountId": None,
                    "attributeId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                    "fsName": "fsName",
                    "fsMappingId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                }
            ]
        }
        
        request = {
            "body": json.dumps(body)
        }

        result = handler(request,
        LambdaContext())

        assert 200 == result['statusCode']

