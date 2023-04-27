import json
import unittest

from .accounts_base import AccountsTestBase
from ...data import get_with_fund_id, get_without_fund_id, LambdaContext


class TestAccountsGetById(AccountsTestBase):

    def test_goodApiRequest(self):
        from accounts import get
        result = get(get_with_fund_id, LambdaContext())

        self.assertEqual(result['statusCode'], 200)

    def test_noFundId(self):
        from accounts import get
        result = get(get_without_fund_id, LambdaContext())

        self.assertEqual(result['statusCode'], 400)

    def test_isJsonEncodable(self):
        from accounts import get
        result = get(get_with_fund_id, LambdaContext())

        json_ = json.dumps(result)

if __name__ == "__main__":
    unittest.main()

