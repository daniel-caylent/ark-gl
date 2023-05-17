import json

from tests.app.data import LambdaContext, commit_account

from .accounts_test_base import AccountsTestBase

class TestAccountsState(AccountsTestBase):

    def test_get(self):
        from app.v1.accounts.state.put import handler
        result = handler(commit_account, LambdaContext())
        assert 200 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.accounts.state.put import handler
        result = handler({}, LambdaContext())
        json.dumps(result)