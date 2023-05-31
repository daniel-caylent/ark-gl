from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR

MODELS = str(PurePath(APP_DIR, 'journal_entries', 'put'))
PATHS = [MODELS]

class TestJournalEntriesState(TestBase(PATHS)):

    def test_good_api_request(self):
        from app.v1.journal_entries.put.state import handler
        request = {
            "body": "{\"state\": \"COMMITTED\"}",
            "pathParameters": {
                "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }

        result = handler(request, LambdaContext())
        assert 200 == result['statusCode']

    def test_invalid(self):
        from app.v1.journal_entries.put.state import handler
        request = {
            "body": "{\"state\": \"POSTED\"}",
            "pathParameters": {
                "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_bad_id_request(self):
        from app.v1.journal_entries.put.state import handler
        request = {
            "body": "{\"state\": \"COMMITTED\"}",
            "pathParameters": {
                "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_missing_id(self):
        from app.v1.journal_entries.put.state import handler
        request = {
            "body": "{\"state\": \"COMMITTED\"}",
            "pathParameters": {
                "journalEntryI": "a92bde1e-7825-429d-aaae-909f2d7a8df"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_missing_path_params(self):
        from app.v1.journal_entries.put.state import handler
        request = {
            "body": "{\"state\": \"COMMITTED\"}",
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_commit_committed(self):
        from app.v1.journal_entries.put.state import handler
        request = {
            "body": "{\"state\": \"COMMITTED\"}",
            "pathParameters": {
                "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df2"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_invalid_body(self):
        from app.v1.journal_entries.put.state import handler
        request = {
            "body": "\"state\": \"COMMITTED\"}",
            "pathParameters": {
                "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df2"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_no_state(self):
        from app.v1.journal_entries.put.state import handler
        request = {
            "body": "\"stat\": \"COMMITTED\"}",
            "pathParameters": {
                "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df2"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']
