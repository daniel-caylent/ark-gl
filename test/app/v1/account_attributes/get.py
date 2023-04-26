import unittest

from account_attributes import get

from ...data import LambdaContext


class TestAccountAttributesGet(unittest.TestCase):
    
    def test_get(self):
        result = get({}, LambdaContext())
        self.assertEqual(200, result['statusCode'])

if __name__ == "__main__":
    unittest.main()
