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
