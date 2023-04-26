import unittest

from ...data import LambdaContext
from .account_attributes_base import AccountAttributesTestBase

class TestAccountAttributesGet(AccountAttributesTestBase):
    
    def test_get(self):
        from account_attributes import get
        result = get({}, LambdaContext())
        self.assertEqual(200, result['statusCode'])

if __name__ == "__main__":
    unittest.main()
