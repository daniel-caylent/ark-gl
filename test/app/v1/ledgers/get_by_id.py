import json
import unittest

from .ledgers_base import LedgersTestBase
from ...data import (
    get_with_account_id,
    get_without_fund_id,
    get_with_bad_account_id,
    LambdaContext
)


class TestLedgersGetById(LedgersTestBase):

    def test_goodApiRequest(self):
        from ledgers import get_by_id
        result = get_by_id(get_with_account_id, LambdaContext())

        self.assertEqual(result['statusCode'], 200)

    def test_noAccountId(self):
        from ledgers import get_by_id
        result = get_by_id(get_without_fund_id, LambdaContext())

        self.assertEqual(result['statusCode'], 400)

    def test_badAccountId(self):
        from ledgers import get_by_id
        result = get_by_id(get_with_bad_account_id, LambdaContext())
        self.assertEqual(result['statusCode'], 404)

    def test_isJsonEncodable(self):
        from ledgers import get_by_id
        result = get_by_id(get_with_account_id, LambdaContext())

        json_ = json.dumps(result)

if __name__ == "__main__":
    unittest.main()

