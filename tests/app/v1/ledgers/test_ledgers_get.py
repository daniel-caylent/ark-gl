import json
from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'ledgers', 'get'))
PATHS = [MODELS, APP_SHARED_LAYER]

class TestLedgersGet(TestBase(PATHS)):

    def test_good_api_request(self):
        from app.v1.ledgers.get.get import handler
        request = {
            "queryStringParameters": {
                "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                "clientId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }

        result = handler(request, LambdaContext())

        assert 200 == result['statusCode']

    def test_no_fund_id(self):
        from app.v1.ledgers.get.get import handler
        request = {
            "queryStringParameters": {
                "clientId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }

        result = handler(request, LambdaContext())

        assert 200 == result['statusCode']

    def test_no_fund_or_client_id(self):
        from app.v1.ledgers.get.get import handler
        request = {
            "queryStringParameters": {
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_bad_fund_id(self):
        from app.v1.ledgers.get.get import handler

        request = {
            "queryStringParameters": {
                "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df",
                "clientId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }
        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_bad_client_id(self):
        from app.v1.ledgers.get.get import handler

        request = {
            "queryStringParameters": {
                "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                "clientId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
            }
        }
        result = handler(request, LambdaContext())

        assert 200 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.ledgers.get.get import handler

        request = {
            "queryStringParameters": {
                "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                "clientId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }
        result = handler(request, LambdaContext())

        json.dumps(result)
