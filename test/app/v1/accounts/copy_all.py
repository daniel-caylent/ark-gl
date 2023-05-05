import json
import unittest

from .accounts_base import AccountsTestBase
from ...data import (
    LambdaContext,
    good_copy
)


class TestAccountsCopy(AccountsTestBase):

    def test_goodApiRequest(self):
        from accounts import copy_all
        result = copy_all(good_copy, LambdaContext())

        self.assertEqual(result['statusCode'], 201)

    def test_isJsonEncodable(self):
        from accounts import copy_all
        result = copy_all(good_copy, LambdaContext())

        json.dumps(result)

if __name__ == "__main__":
    unittest.main()
