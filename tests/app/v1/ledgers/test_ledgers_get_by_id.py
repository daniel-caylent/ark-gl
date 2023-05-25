import json
from pathlib import PurePath

from tests.app.data import (
    get_with_account_id,
    get_without_fund_id,
    get_with_bad_account_id,
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR

MODELS = str(PurePath(APP_DIR, 'ledgers', 'get'))
PATHS = [MODELS]

class TestLedgersPost(TestBase(PATHS)):

    def test_good_api_request(self):
        from app.v1.ledgers.get.get_by_id import handler
        result = handler(get_with_account_id, LambdaContext())
        assert 200 == result['statusCode']

    def test_no_account_id(self):
        from app.v1.ledgers.get.get_by_id import handler
        result = handler(get_without_fund_id, LambdaContext())
        assert 400 == result['statusCode']

    def test_bad_account_id(self):
        from app.v1.ledgers.get.get_by_id import handler
        result = handler(get_with_bad_account_id, LambdaContext())
        assert 404 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.ledgers.get.get_by_id import handler
        result = handler(get_with_account_id, LambdaContext())
        json.dumps(result)
