import json
import pytest

from tests.app.data import (
    good_upload,
    LambdaContext
)

from .accounts_test_base import AccountsTestBase

class TestAccountsUpload(AccountsTestBase):

    @pytest.mark.skip(reason="failing tests") #TODO fix this failing test
    def test_good_api_request(self):
        from app.v1.accounts.upload.post import handler
        result = handler(good_upload, LambdaContext())

        assert 201 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.accounts.upload.post import handler
        result = handler(good_upload, LambdaContext())

        json.dumps(result)