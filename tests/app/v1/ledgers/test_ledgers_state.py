import json
import pytest

from tests.app.data import (
    LambdaContext
)

from .ledgers_test_base import LedgersTestBase

class TestLedgersState(LedgersTestBase):

    def test_good_state(self):
      from app.v1.ledgers import state
      body = {
         "state": "COMMITTED"
      }

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": json.dumps(body)
      }
      response = state(request, LambdaContext())

      assert 200 == response['statusCode']

    def test_bad_state(self):
      from app.v1.ledgers import state
      body = {
         "state": "bad"
      }

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": json.dumps(body)
      }
      response = state(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_bad_body(self):
      from app.v1.ledgers import state
      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = state(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_bad_params(self):
      from app.v1.ledgers import state
      request = {
         "pathParameters": {
            "ledgerI": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = state(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_no_params(self):
      from app.v1.ledgers import state
      request = {
         "pathParameters": None,
         "body": None
      }
      response = state(request, LambdaContext())

      assert 400 == response['statusCode']
