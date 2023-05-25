import json
from pathlib import PurePath

from tests.app.data import (
    get_with_fund_id,
    get_without_fund_id,
    get_with_non_uuid_fund_id,
    LambdaContext
)

from .accounts_test_base import AccountsTestBase

class TestAccountsGet(AccountsTestBase):

    def test_good_api_request(self):
        from app.v1.accounts.get.get import handler
        result = handler(get_with_fund_id, LambdaContext())
        assert 200 == result['statusCode']

    def test_no_fund_id(self):
        from app.v1.accounts.get.get import handler
        result = handler(get_without_fund_id, LambdaContext())

        assert 400 == result['statusCode']

    def test_bad_fund_id(self):
        from app.v1.accounts.get.get import handler
        result = handler(get_with_non_uuid_fund_id, LambdaContext())

        assert 400 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.accounts.get.get import handler
        result = handler(get_with_fund_id, LambdaContext())

        json.dumps(result)