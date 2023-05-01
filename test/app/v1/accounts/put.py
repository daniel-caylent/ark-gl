import unittest

from .accounts_base import AccountsTestBase
from ...data import (
    good_post,
    post_with_bad_body,
    post_with_duplicate_name,
    post_with_duplicate_account_number,
    post_without_fund_id,
    LambdaContext
)

class TestAccountsPut(AccountsTestBase):

    def test_goodPut(self):
        from accounts import put
        result = put(good_post, LambdaContext())
        self.assertEqual(result['statusCode'], 201)

    def test_putWithBadBody(self):
        from accounts import put
        result = put(post_with_bad_body, LambdaContext())
        self.assertEqual(result['statusCode'], 400)

    def test_putWithDuplicateName(self):
        from accounts import put
        result = put(post_with_duplicate_name, LambdaContext())
        self.assertEqual(result['statusCode'], 409)

    def test_putWithDuplicateAccountNumber(self):
        from accounts import put
        result = put(post_with_duplicate_account_number, LambdaContext())
        self.assertEqual(result['statusCode'], 409)

if __name__ == "__main__":
    unittest.main()
