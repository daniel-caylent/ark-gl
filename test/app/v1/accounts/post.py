import unittest

from accounts import post

from ...data import (
    post_with_good_body,
    LambdaContext
)

class TestAccountsPost(unittest.TestCase):

    def test_goodApiRequest(self):
        result = post(post_with_good_body, LambdaContext())

        self.assertEqual(result['statusCode'], 201)

if __name__ == "__main__":
    unittest.main()

