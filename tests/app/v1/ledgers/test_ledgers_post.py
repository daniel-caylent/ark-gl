import json
import pytest

from tests.app.data import (
    LambdaContext
)

from .ledgers_test_base import LedgersTestBase

class TestLedgersPost(LedgersTestBase):

    def test_good_post(self):
      from app.v1.ledgers import post
      body = {
         "glDescription": "test",
         "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
         "glName": "unique",
         "currencyName": "USD",
         "currencyDecimal": 2
      }

      request = {
         "body": json.dumps(body)
      }
      response = post(request, LambdaContext())
      assert 201 == response['statusCode']

    def test_duplicate_name(self):
      from app.v1.ledgers import post
      body = {
         "glDescription": "test",
         "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
         "glName": "duplicate",
         "currencyName": "USD",
         "currencyDecimal": 2
      }

      request = {
         "body": json.dumps(body)
      }
      response = post(request, LambdaContext())
      assert 409 == response['statusCode']


    def test_bad_fund_uuid(self):
      from app.v1.ledgers import post
      body = {
         "glDescription": "test",
         "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df",
         "glName": "duplicate",
         "currencyName": "USD",
         "currencyDecimal": 2
      }

      request = {
         "body": json.dumps(body)
      }
      response = post(request, LambdaContext())
      assert 400 == response['statusCode']
