from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'journal_entries', 'post'))
PATHS = [MODELS, APP_SHARED_LAYER]

class TestJournalEntriesUpload(TestBase(PATHS)):

    def test_success(self):
        from app.v1.journal_entries.post.upload import handler
        request = {
            "body": "{\"signedS3Url\": \"URL\"}"
        }

        def mock_return(*args, **kwargs):
            class Response:
                def read(*args, **kwargs):
                    return b"""{
              "journalEntries": [
                {
                  "fundId": "e6a9ebc1-59e3-4cd7-b16c-45ae6e0e05ba",
                  "clientId": "90b25612-955c-40b6-961a-c15f977d3062",
                  "ledgerName": "Unique Ledger Name",
                  "date": "2017-01-01",
                  "memo": "These charges describe catered lunches.",
                  "adjustingJournalEntry": true,
                  "reference": "",
                  "journalEntryNum": 13455,
                  "lineItems": [
                    {
                      "accountName": "account name-2",
                      "memo": "These charges describe catered Pizza.",
                      "entityId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
                      "amount": 10012,
                      "type": "CREDIT"
                    },
                    {
                      "accountName": "account name",
                      "memo": "These charges describe catered Pizza.",
                      "entityId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
                      "amount": 10012,
                      "type": "DEBIT"
                    }
                  ]
                }
              ]
            }"""
                
            return Response()

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_return)

        result = handler(request, LambdaContext())

        print(result)
        assert 201 == result['statusCode']
