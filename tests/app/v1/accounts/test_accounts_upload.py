import os
import json
from pathlib import PurePath

import pytest

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'accounts', 'post'))
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

class TestAccountsUpload(TestBase(PATHS)):

    def test_good_upload(self):
        from app.v1.accounts.post.upload import handler
        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "accts.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())
        assert 201 == result['statusCode']

    def test_malformed(self):
        from app.v1.accounts.post.upload import handler
        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "accts_malformed.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_missing_accountNo(self):
        from app.v1.accounts.post.upload import handler
        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "accts_missing_accountNo.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']


    def test_empty_accounts(self):
        from app.v1.accounts.post.upload import handler
        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "accts_empty_accounts.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']


    def test_with_parents(self):
        from app.v1.accounts.post.upload import handler
        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "accounts_parents.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())
        assert 201 == result['statusCode']


    def test_with_fs_mapping(self):
        from app.v1.accounts.post.upload import handler
        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "accts_fs_mapping.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())
        assert 201 == result['statusCode']


    def test_duplicate_name(self):
        from app.v1.accounts.post.upload import handler
        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "accounts_name_dup.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_duplicate_number(self):
        from app.v1.accounts.post.upload import handler
        body = {
            "signedS3Url": str(PurePath(DATA_DIR, "accounts_number_dup.json"))
        }
        request = {
            "body": json.dumps(body)
        }

        mp = pytest.MonkeyPatch()
        mp.setattr("urllib.request.urlopen", mock_urlopen)

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']
