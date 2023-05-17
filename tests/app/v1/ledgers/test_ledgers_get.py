import json
import pytest

from tests.app.data import (
    get_with_fund_id,
    get_without_fund_id,
    get_with_non_uuid_fund_id,
    LambdaContext
)

from .ledgers_test_base import LedgersTestBase

class TestLedgersGet(LedgersTestBase):

    @pytest.mark.skip(reason="failing tests") #TODO fix this failing test
    def test_good_api_request(self):
        from app.v1.ledgers.get.get import handler
        result = handler(get_with_fund_id, LambdaContext())

        assert 200 == result['statusCode']

    def test_no_fund_id(self):
        from app.v1.ledgers.get.get import handler
        result = handler(get_without_fund_id, LambdaContext())

        assert 400 == result['statusCode']

    def test_bad_fund_id(self):
        from app.v1.ledgers.get.get import handler
        result = handler(get_with_non_uuid_fund_id, LambdaContext())

        assert 400 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.ledgers.get.get import handler
        result = handler(get_with_fund_id, LambdaContext())

        json.dumps(result)
