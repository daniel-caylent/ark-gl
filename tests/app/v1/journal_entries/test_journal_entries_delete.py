from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR

MODELS = str(PurePath(APP_DIR, 'journal_entries', 'delete'))
PATHS = [MODELS]

class TestJournalEntriesDelete(TestBase(PATHS)):

    def test_good_api_request(self):
        from app.v1.journal_entries.delete.delete import handler
        request = {
            "pathParameters": {
                "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }

        result = handler(request, LambdaContext())

        print(result)
        assert 200 == result['statusCode']

    def test_bad_id_request(self):
        from app.v1.journal_entries.delete.delete import handler
        request = {
            "pathParameters": {
                "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_missing_id(self):
        from app.v1.journal_entries.delete.delete import handler
        request = {
            "pathParameters": {
                "journalEntryI": "a92bde1e-7825-429d-aaae-909f2d7a8df"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_missing_path_params(self):
        from app.v1.journal_entries.delete.delete import handler
        request = {
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_delete_committed(self):
        from app.v1.journal_entries.delete.delete import handler
        request = {
            "pathParameters": {
                "journalEntryId": "a92bde1e-7825-429d-aaae-909f2d7a8df2"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']
