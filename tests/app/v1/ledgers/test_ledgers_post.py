import json
from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'ledgers', 'post'))
PATHS = [MODELS, APP_SHARED_LAYER]

class TestLedgersPost(TestBase(PATHS)):

    def test_good_post(self):
      from app.v1.ledgers.post.post import handler
      body = {
         "glDescription": "test",
         "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
         "clientId": "d4b26dc7-e51a-11ed-aede-0247c1ed2eeb", 
         "glName": "unique",
         "currencyName": "USD",
         "currencyDecimal": 2
      }

      request = {
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())
      assert 201 == response['statusCode']

    def test_duplicate_name(self):
      from app.v1.ledgers.post.post import handler
      body = {
         "glDescription": "test",
         "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
         "clientId": "d4b26dc7-e51a-11ed-aede-0247c1ed2eeb", 
         "glName": "duplicate",
         "currencyName": "USD",
         "currencyDecimal": 2
      }

      request = {
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())
      assert 409 == response['statusCode']


    def test_bad_fund_uuid(self):
      from app.v1.ledgers.post.post import handler
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
      response = handler(request, LambdaContext())
      assert 400 == response['statusCode']
