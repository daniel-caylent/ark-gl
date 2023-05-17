import json

from tests.app.data import (
    get_with_account_id,
    get_without_fund_id,
    get_with_bad_account_id,
    LambdaContext
)

from .accounts_test_base import AccountsTestBase

class TestAccountsGetById(AccountsTestBase):

    def test_good_api_request(self):
        from app.v1.accounts.get_by_id.get import handler
        result = handler(get_with_account_id, LambdaContext())
        assert 200 == result['statusCode']

    def test_no_account_id(self):
        from app.v1.accounts.get_by_id.get import handler
        result = handler(get_without_fund_id, LambdaContext())
        assert 400 == result['statusCode']

    def test_bad_account_id(self):
        from app.v1.accounts.get_by_id.get import handler
        result = handler(get_with_bad_account_id, LambdaContext())
        assert 404 == result['statusCode']

    def test_non_uui_id(self):
        from app.v1.accounts.get_by_id.get import handler
        result = handler(get_with_bad_account_id, LambdaContext())
        assert 404 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.accounts.get_by_id.get import handler
        result = handler(get_with_account_id, LambdaContext())
        json.dumps(result)