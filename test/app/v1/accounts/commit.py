import unittest

from .accounts_base import AccountsTestBase
from ...data import (
    get_with_account_id,
    get_with_non_uuid_account_id,
    LambdaContext
)

class TestAccountsCommit(AccountsTestBase):

    def test_goodCommit(self):
        from accounts import commit
        result = commit(get_with_account_id, LambdaContext())
        self.assertEqual(result['statusCode'], 200)

    def test_commitWithBadUuid(self):
        from accounts import commit
        result = commit(get_with_non_uuid_account_id, LambdaContext())
        self.assertEqual(result['statusCode'], 400)

if __name__ == "__main__":
    unittest.main()
