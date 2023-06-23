import json
from pathlib import PurePath

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER, MOCK_DIR

MODELS = str(PurePath(APP_DIR, 'ledgers', 'state'))
PATHS = [MODELS, APP_SHARED_LAYER, MOCK_DIR]

class TestLedgersState(TestBase(PATHS)):

    def test_good_state(self):
      from app.v1.ledgers.put.state import handler
      body = {
         "state": "POSTED"
      }

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())
      assert 200 == response['statusCode']

    def test_bad_state(self):
      from app.v1.ledgers.put.state import handler
      body = {
         "state": "bad"
      }

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_bad_body(self):
      from app.v1.ledgers.put.state import handler
      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_bad_params(self):
      from app.v1.ledgers.put.state import handler
      request = {
         "pathParameters": {
            "ledgerI": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_no_params(self):
      from app.v1.ledgers.put.state import handler
      request = {
         "pathParameters": None,
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']
