import json
from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'journal_entries', 'put'))
PATHS = [MODELS, APP_SHARED_LAYER]

class TestJournalEntriesPut(TestBase(PATHS)):

    def test_success(self):
        from app.v1.journal_entries.put.put import handler
        request = {
            "body": """{
              \"date\": \"10-19-1991\",
              \"reference\": \"Reference\",
              \"memo\": \"memo\",
              \"adjustingJournalEntry\": false,
              \"attachments\": [
                  {
                      \"documentId\": \"This is the id\",
                      \"documentMemo\": \"Memo\"
                  }
              ],
              \"lineItems\": [
                  {
                      \"accountNo\": \"5555\",
                      \"memo\": \"memo\",
                      \"type\": \"CREDIT\",
                      \"amount\": 1000,
                      \"entityId\": \"1234123\"
                  },
                  {
                      \"accountNo\": \"5555\",
                      \"memo\": \"memo\",
                      \"type\": \"DEBIT\",
                      \"amount\": \"1000\",
                      \"entityId\": \"1234123\"
                  }
              ]
          }""",
          "pathParameters": {
            "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
          }
        }

        result = handler(request, LambdaContext())
        print(result)

        assert 200 == result['statusCode']


    def test_uneven_line_items(self):
        from app.v1.journal_entries.put.put import handler
        request = {
            "body": """{
              \"date\": \"10-19-1991\",
              \"reference\": \"Reference\",
              \"memo\": \"memo\",
              \"adjustingJournalEntry\": false,
              \"attachments\": [
                  {
                      \"documentId\": \"This is the id\",
                      \"documentMemo\": \"Memo\"
                  }
              ],
              \"lineItems\": [
                  {
                      \"accountNo\": \"5555\",
                      \"memo\": \"memo\",
                      \"type\": \"CREDIT\",
                      \"amount\": 1000,
                      \"entityId\": \"1234123\"
                  },
                  {
                      \"accountNo\": \"5555\",
                      \"memo\": \"memo\",
                      \"type\": \"DEBIT\",
                      \"amount\": \"1001\",
                      \"entityId\": \"1234123\"
                  }
              ]
          }""",
          "pathParameters": {
            "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
          }
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_bad_body(self):
        from app.v1.journal_entries.put.put import handler
        request = {
            "body": """{
              \"date\": True,
              \"reference\": \"Reference\",
              \"memo\": \"memo\",
              \"adjustingJournalEntry\": false,
              \"attachments\": [
                  {
                      \"documentId\": \"This is the id\",
                      \"documentMemo\": \"Memo\"
                  }
              ],
              \"lineItems\": [
                  {
                      \"accountNo\": \"5555\",
                      \"memo\": \"memo\",
                      \"type\": \"CREDIT\",
                      \"amount\": 1000,
                      \"entityId\": \"1234123\"
                  },
                  {
                      \"accountNo\": \"5555\",
                      \"memo\": \"memo\",
                      \"type\": \"DEBIT\",
                      \"amount\": \"1001\",
                      \"entityId\": \"1234123\"
                  }
              ]
          }""",
          "pathParameters": {
            "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
          }
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_update_committed(self):
        from app.v1.journal_entries.put.put import handler
        request = {
            "body": """{
              \"reference\": \"Reference\",
              \"memo\": \"memo\",
              \"adjustingJournalEntry\": false
          }""",
          "pathParameters": {
            "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df2"
          }
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']
