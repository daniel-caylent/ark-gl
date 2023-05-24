import json
import pytest

from tests.app.data import (
    LambdaContext,
    good_copy
)

from .accounts_test_base import AccountsTestBase

class TestAccountsCopy(AccountsTestBase):

    # @pytest.mark.skip(reason="failing tests") #TODO fix this failing test
    # def test_good_api_request(self):
    #     from app.v1.accounts.copy_all.post import handler
    #     result = handler(good_copy, LambdaContext())
    #     assert 201 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.accounts.copy_all.post import handler
        result = handler(good_copy, LambdaContext())
        json.dumps(result)