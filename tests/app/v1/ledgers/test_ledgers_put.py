import json
import pytest

from tests.app.data import (
    LambdaContext
)

from .ledgers_test_base import LedgersTestBase

class TestLedgersPut(LedgersTestBase):

    def test_good_put(self):
      from app.v1.ledgers import put
      body = {
         "glDescription": "test"
      }

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": json.dumps(body)
      }
      response = put(request, LambdaContext())

      assert 200 == response['statusCode']

    def test_duplicat_name(self):
      from app.v1.ledgers import put
      body = {
         "glName": "duplicate"
      }

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": json.dumps(body)
      }
      response = put(request, LambdaContext())

      assert 409 == response['statusCode']

    def test_all_fields(self):
      from app.v1.ledgers import put
      body = {
        "glName": "Non-duplicate",
        "glDescription": "none",
        "currencyName": "USD",
        "currencyDecimal": 3
      }

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": json.dumps(body)
      }
      response = put(request, LambdaContext())

      assert 200 == response['statusCode']

    def test_bad_body(self):
      from app.v1.ledgers import put
      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = put(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_bad_params(self):
      from app.v1.ledgers import put
      request = {
         "pathParameters": {
            "ledgerI": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = put(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_no_params(self):
      from app.v1.ledgers import put
      request = {
         "pathParameters": None,
         "body": None
      }
      response = put(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_empty_body(self):
      from app.v1.ledgers import put
      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": {}
      }
      response = put(request, LambdaContext())

      assert 400 == response['statusCode']