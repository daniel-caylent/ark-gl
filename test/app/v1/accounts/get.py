import unittest

from accounts import get

from ...data import get_with_fund_id, get_without_fund_id, LambdaContext

class TestAccountsGet(unittest.TestCase):

    def test_goodApiRequest(self):
        lc = LambdaContext()
        result = get(get_with_fund_id, lc)

        self.assertEqual(result['statusCode'], 200)

    def test_noFundId(self):
        lc = LambdaContext()
        result = get(get_without_fund_id, lc)

        self.assertEqual(result['statusCode'], 400)

if __name__ == "__main__":
    unittest.main()

