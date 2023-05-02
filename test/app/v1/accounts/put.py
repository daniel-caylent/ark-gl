import unittest

from .accounts_base import AccountsTestBase
from ...data import (
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

class TestAccountsPut(AccountsTestBase):

    def test_goodPut(self):
        from accounts import put
        result = put(good_put, LambdaContext())
        self.assertEqual(result['statusCode'], 200)

    def test_putWithoutAccountNumber(self):
        from accounts import put
        result = put(put_without_account_number, LambdaContext())
        self.assertEqual(result['statusCode'], 400)

    def test_putWithParentId(self):
        from accounts import put
        result = put(put_with_parent_id, LambdaContext())
        self.assertEqual(result['statusCode'], 200)

    def test_putWithBadUuid(self):
        from accounts import put
        result = put(put_with_bad_uuid, LambdaContext())
        self.assertEqual(result['statusCode'], 400)

    def test_putWithCommittedAccount(self):
        from accounts import put
        result = put(put_with_committed_account, LambdaContext())
        self.assertEqual(result['statusCode'], 400)

    def test_putWithCommittedAccountAllowed(self):
        from accounts import put
        result = put(put_with_committed_account_allowed, LambdaContext())
        self.assertEqual(result['statusCode'], 200)

    def test_putWithBadBody(self):
        from accounts import put
        result = put(put_with_bad_body, LambdaContext())
        self.assertEqual(result['statusCode'], 400)

    def test_putWithDuplicateName(self):
        from accounts import put
        result = put(put_with_duplicate_name, LambdaContext())
        self.assertEqual(result['statusCode'], 409)

    def test_putWithDuplicateAccountNumber(self):
        from accounts import put
        result = put(put_with_duplicate_account_number, LambdaContext())
        self.assertEqual(result['statusCode'], 409)

if __name__ == "__main__":
    unittest.main()
