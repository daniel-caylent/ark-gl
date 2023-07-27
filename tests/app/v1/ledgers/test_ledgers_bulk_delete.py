import json
from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_SHARED_LAYER

PATHS = [APP_SHARED_LAYER]

class TestLedgersBulkDelete(TestBase(PATHS)):

    def test_good_post(self):
      from app.v1.ledgers.delete.bulk import handler
      body = {
         "ledgerIds": ["a92bde1e-7825-429d-aaae-909f2d7a8df1"]
      }

      request = {
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())
      assert 200 == response['statusCode']


    def test_missing_ids(self):
      from app.v1.ledgers.delete.bulk import handler
      body = {
         "ledgerIds": []
      }

      request = {
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())
      assert 400 == response['statusCode']


    def test_missing_body(self):
      from app.v1.ledgers.delete.bulk import handler
      request = {
      }

      response = handler(request, LambdaContext())
      assert 400 == response['statusCode']



    def test_no_ledger_found(self):
      from app.v1.ledgers.delete.bulk import handler
      body = {
         "ledgerIds": ["a92bde1e-7825-429d-aaae-909f2d7a8df2"]
      }

      request = {
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())
      assert 404 == response['statusCode']

    def test_delete_posted(self):
      from app.v1.ledgers.delete.bulk import handler
      body = {
         "ledgerIds": ["p7e84f41-eaa5-11ed-9a6e-0a3efd619f29"]
      }

      request = {
         "body": json.dumps(body)
      }
      response = handler(request, LambdaContext())
      assert 400 == response['statusCode']
