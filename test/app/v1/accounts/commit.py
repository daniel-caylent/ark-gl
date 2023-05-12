import unittest

from .accounts_base import AccountsTestBase
from ...data import (
    commit_account,
    bad_commit_account,
    LambdaContext
)

class TestAccountsState(AccountsTestBase):

    def test_goodstate(self):
        from accounts import state
        result = state(commit_account, LambdaContext())
        self.assertEqual(result['statusCode'], 200)

    def test_stateWithBadUuid(self):
        from accounts import state
        result = state(bad_commit_account, LambdaContext())
        self.assertEqual(result['statusCode'], 400)

if __name__ == "__main__":
    unittest.main()
