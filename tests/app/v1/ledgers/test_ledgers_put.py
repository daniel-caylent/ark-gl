import json
from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'ledgers', 'put'))
PATHS = [MODELS, APP_SHARED_LAYER]

class TestLedgersPut(TestBase(PATHS)):

    def test_good_put(self):
      from app.v1.ledgers.put.put import handler
      body = {
         "glDescription": "test"
      }

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())

      assert 200 == response['statusCode']

    def test_duplicat_name(self):
      from app.v1.ledgers.put.put import handler
      body = {
         "glName": "duplicate"
      }

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())

      assert 409 == response['statusCode']

    def test_all_fields(self):
      from app.v1.ledgers.put.put import handler
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
      response = handler(request, LambdaContext())

      assert 200 == response['statusCode']

    def test_bad_body(self):
      from app.v1.ledgers.put.put import handler
      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_bad_params(self):
      from app.v1.ledgers.put.put import handler
      request = {
         "pathParameters": {
            "ledgerI": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_no_params(self):
      from app.v1.ledgers.put.put import handler
      request = {
         "pathParameters": None,
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_empty_body(self):
      from app.v1.ledgers.put.put import handler
      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": {}
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']