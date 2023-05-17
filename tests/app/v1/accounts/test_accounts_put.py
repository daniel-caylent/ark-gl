import pytest

from tests.app.data import (
    good_put,
    put_with_bad_body,
    put_with_duplicate_name,
    put_with_duplicate_account_number,
    put_without_account_number,
    put_with_bad_uuid,
    put_with_committed_account,
    put_with_committed_account_allowed,
    put_with_parent_id,
    LambdaContext
)

from .accounts_test_base import AccountsTestBase

class TestAccountsPut(AccountsTestBase):

    def test_good_put(self):
        from app.v1.accounts.put.put import handler
        result = handler(good_put, LambdaContext())
        assert 200 == result['statusCode']

    def test_put_without_account_number(self):
        from app.v1.accounts.put.put import handler
        result = handler(put_without_account_number, LambdaContext())
        assert 400 == result['statusCode']

    def test_put_with_parent_id(self):
        from app.v1.accounts.put.put import handler
        result = handler(put_with_parent_id, LambdaContext())
        assert 200 == result['statusCode']

    def test_put_with_bad_uuid(self):
        from app.v1.accounts.put.put import handler
        result = handler(put_with_bad_uuid, LambdaContext())
        assert 400 == result['statusCode']

    @pytest.mark.skip(reason="failing test") #TODO fix this failing test
    def test_put_with_committed_account(self):
        from app.v1.accounts.put.put import handler
        result = handler(put_with_committed_account, LambdaContext())
        assert 400 == result['statusCode']

    def test_put_with_committed_account_allowed(self):
        from app.v1.accounts.put.put import handler
        result = handler(put_with_committed_account_allowed, LambdaContext())
        assert 200 == result['statusCode']

    def test_put_with_bad_body(self):
        from app.v1.accounts.put.put import handler
        result = handler(put_with_bad_body, LambdaContext())
        assert 400 == result['statusCode']

    def test_put_with_duplicate_name(self):
        from app.v1.accounts.put.put import handler
        result = handler(put_with_duplicate_name, LambdaContext())
        assert 409 == result['statusCode']

    def test_put_with_duplicate_account_number(self):
        from app.v1.accounts.put.put import handler
        result = handler(put_with_duplicate_account_number, LambdaContext())
        assert 409 == result['statusCode']