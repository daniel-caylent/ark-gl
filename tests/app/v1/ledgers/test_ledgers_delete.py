import pytest

from tests.app.data import (
    LambdaContext
)

from .ledgers_test_base import LedgersTestBase

class TestLedgersDelete(LedgersTestBase):

    def test_good_delete(self):
      from app.v1.ledgers.delete.delete import handler

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         }
      }

      response = handler(request, LambdaContext())

      assert 200 == response['statusCode']

    def test_bad_uuid(self):
      from app.v1.ledgers.delete.delete import handler

      request = {
         "pathParameters": {
            "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
         }
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_bad_params(self):
      from app.v1.ledgers.delete.delete import handler
      request = {
         "pathParameters": {
            "ledgerI": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
         },
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']

    def test_no_params(self):
      from app.v1.ledgers.delete.delete import handler
      request = {
         "pathParameters": None,
         "body": None
      }
      response = handler(request, LambdaContext())

      assert 400 == response['statusCode']
