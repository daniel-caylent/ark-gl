from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'journal_entries', 'post'))
PATHS = [MODELS, APP_SHARED_LAYER]

class TestJournalEntriesPost(TestBase(PATHS)):

    def test_success(self):
        from app.v1.journal_entries.post.post import handler
        request = {
            "body": """{
              \"ledgerId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",
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
                      \"entityId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"
                  },
                  {
                      \"accountNo\": \"5555\",
                      \"memo\": \"memo\",
                      \"type\": \"DEBIT\",
                      \"amount\": \"1000\",
                      \"entityId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"
                  }
              ]
          }"""
        }

        result = handler(request, LambdaContext())
        assert 201 == result['statusCode']


    def test_uneven_line_items(self):
        from app.v1.journal_entries.post.post import handler
        request = {
            "body": """{
              \"ledgerId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",
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
                      \"entityId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"
                  },
                  {
                      \"accountNo\": \"5555\",
                      \"memo\": \"memo\",
                      \"type\": \"DEBIT\",
                      \"amount\": \"1001\",
                      \"entityId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"
                  }
              ]
          }"""
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_bad_body(self):
        from app.v1.journal_entries.post.post import handler
        request = {
            "body": """{
              \"ledgerId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",
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
                      \"entityId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"
                  },
                  {
                      \"accountNo\": \"5555\",
                      \"memo\": \"memo\",
                      \"type\": \"DEBIT\",
                      \"amount\": \"1001\",
                      \"entityId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"
                  }
              ]
          }"""
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']
