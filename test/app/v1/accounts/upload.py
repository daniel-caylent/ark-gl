import json
import unittest

from .accounts_base import AccountsTestBase
from ...data import (
    LambdaContext,
    good_upload
)


class TestAccountsUpload(AccountsTestBase):

    def test_goodApiRequest(self):
        from accounts import upload
        result = upload(good_upload, LambdaContext())

        self.assertEqual(result['statusCode'], 201)

    def test_isJsonEncodable(self):
        from accounts import upload
        result = upload(good_upload, LambdaContext())

        json.dumps(result)

if __name__ == "__main__":
    unittest.main()

