import json
import unittest

from .ledgers_base import LedgersTestBase
from ...data import get_with_fund_id, get_without_fund_id, get_with_non_uuid_fund_id, LambdaContext


class TestLedgersGet(LedgersTestBase):

    def test_goodApiRequest(self):
        
        from ledgers import get
        result = get(get_with_fund_id, LambdaContext())
        self.assertEqual(result['statusCode'], 200)

    def test_noFundId(self):
        from ledgers import get
        result = get(get_without_fund_id, LambdaContext())

        self.assertEqual(result['statusCode'], 400)

    def test_badFundId(self):
        from ledgers import get
        result = get(get_with_non_uuid_fund_id, LambdaContext())

        self.assertEqual(result['statusCode'], 400)

    def test_isJsonEncodable(self):
        from ledgers import get
        result = get(get_with_fund_id, LambdaContext())

        json.dumps(result)

if __name__ == "__main__":
    unittest.main()
