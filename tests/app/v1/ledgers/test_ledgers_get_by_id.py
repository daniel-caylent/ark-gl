import json
from pathlib import PurePath

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'ledgers', 'get'))
PATHS = [MODELS, APP_SHARED_LAYER]

class TestLedgersPost(TestBase(PATHS)):

    def test_good_api_request(self):
        request = {
            "pathParameters": {
                "ledgerId":  "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }

        from app.v1.ledgers.get.get_by_id import handler
        result = handler(request, LambdaContext())
        assert 200 == result['statusCode']

    def test_no_ledger_id(self):
        request = {
            "pathParameters": {}
        }
        from app.v1.ledgers.get.get_by_id import handler
        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_bad_ledger_id(self):
        request = {
            "pathParameters": {
                "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df2"
            }
        }

        from app.v1.ledgers.get.get_by_id import handler
        result = handler(request, LambdaContext())
        assert 404 == result['statusCode']

    def test_is_json_encodable(self):
        request = {
            "pathParameters": {
                "ledgerId":  "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }
        from app.v1.ledgers.get.get_by_id import handler
        result = handler(request, LambdaContext())
        json.dumps(result)
