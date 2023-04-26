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

class TestAccountsPost(AccountsTestBase):

    def test_goodPost(self):
        from accounts import post
        result = post(good_post, LambdaContext())
        self.assertEqual(result['statusCode'], 201)

    def test_postWithBadBody(self):
        from accounts import post
        result = post(post_with_bad_body, LambdaContext())
        self.assertEqual(result['statusCode'], 400)

    def test_postWithoutFundId(self):
        from accounts import post
        result = post(post_without_fund_id, LambdaContext())
        self.assertEqual(result['statusCode'], 400)

    def test_postWithDuplicateName(self):
        from accounts import post
        result = post(post_with_duplicate_name, LambdaContext())
        self.assertEqual(result['statusCode'], 409)

    def test_postWithDuplicateAccountNumber(self):
        from accounts import post
        result = post(post_with_duplicate_account_number, LambdaContext())
        self.assertEqual(result['statusCode'], 409)

if __name__ == "__main__":
    unittest.main()
