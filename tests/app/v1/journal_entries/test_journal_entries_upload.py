import json
import os
from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'journal_entries', 'post'))
PATHS = [MODELS, APP_SHARED_LAYER]

DATA_DIR =  str(PurePath(os.path.dirname(__file__), "data"))


def mock_urlopen(url, *args, **kwargs):
    class Response:
        file = url
        def read(self, *args, **kwargs):
            with open(self.file, 'r') as f:
                text = f.read()
            return text.encode()
        
    return Response()

class TestJournalEntriesUpload(TestBase(PATHS)):

    def test_success(self):
        from app.v1.journal_entries.post.upload import handler

        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "je.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())

        print(result)
        assert 201 == result['statusCode']
  
    def test_bad_date(self):
        from app.v1.journal_entries.post.upload import handler

        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "je_bad_date.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']
  
    def test_bad_line_item_type(self):
        from app.v1.journal_entries.post.upload import handler

        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "je_bad_line_item_type.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']
  
    def test_no_line_items(self):
        from app.v1.journal_entries.post.upload import handler

        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "je_no_line_items.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']
  
    def test_bad_decimals(self):
        from app.v1.journal_entries.post.upload import handler

        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "je_bad_decimals.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']

    def test_amount_conversion_int(self):
        from app.v1.journal_entries.post.models import BulkLineItemPost
        func = BulkLineItemPost.convert_amount

        result = func(55, 2)

        assert result == 5500

    def test_amount_conversion_float(self):
        from app.v1.journal_entries.post.models import BulkLineItemPost
        func = BulkLineItemPost.convert_amount

        result = func(55.55, 2)

        assert result == 5555

    def test_amount_conversion_3_decimals(self):
        from app.v1.journal_entries.post.models import BulkLineItemPost
        func = BulkLineItemPost.convert_amount

        result = func(55.555, 3)

        assert result == 55555

    def test_amount_conversion_decimal_mismatch(self):
        from app.v1.journal_entries.post.models import BulkLineItemPost
        func = BulkLineItemPost.convert_amount

        with pytest.raises(Exception):
            func(55.555, 2)

