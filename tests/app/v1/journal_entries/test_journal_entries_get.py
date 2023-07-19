from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'journal_entries', 'get'))
PATHS = [MODELS, APP_SHARED_LAYER]

class TestJournalEntriesGet(TestBase(PATHS)):

    def test_success(self):
        from app.v1.journal_entries.get.get import handler
        request = {
            "queryStringParameters": {
                "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
            }
        }

        result = handler(request, LambdaContext())
        print(result)
        assert 200 == result['statusCode']

    def test_bad_ledger_id(self):
        from app.v1.journal_entries.get.get import handler
        request = {
            "queryStringParameters": {
                "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_missing_ledger_id(self):
        from app.v1.journal_entries.get.get import handler
        request = {
            "queryStringParameters": {
                "ledgerI": "a92bde1e-7825-429d-aaae-909f2d7a8df"
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_missing_query_string_params(self):
        from app.v1.journal_entries.get.get import handler
        request = {}

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']
