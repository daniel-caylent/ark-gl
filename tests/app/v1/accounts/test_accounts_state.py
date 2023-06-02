import json

from tests.app.data import LambdaContext, commit_account

from .accounts_test_base import AccountsTestBase

class TestAccountsState(AccountsTestBase):

    def test_get(self):
        from app.v1.accounts.put.state import handler
        result = handler(commit_account, LambdaContext())
        assert 200 == result['statusCode']

    def test_is_json_encodable(self):
        from app.v1.accounts.put.state import handler
        result = handler({}, LambdaContext())
        json.dumps(result)


    def test_bad_body(self):
      from app.v1.accounts.put.state import handler
      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_bad_params(self):
      from app.v1.accounts.put.state import handler
      request = {
         "pathParameters": {
            "ledgerI": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_no_params(self):
      from app.v1.accounts.put.state import handler
      request = {
         "pathParameters": None,
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']
