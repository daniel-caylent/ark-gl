from pathlib import PurePath

from tests.app.data import (
    LambdaContext
)
from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER, MOCK_DIR

MODELS = str(PurePath(APP_DIR, 'journal_entries', 'post'))
PATHS = [MODELS, APP_SHARED_LAYER, MOCK_DIR]


class Boto3Mocked:

    def put_object(self, **kwargs):
        pass

    def generate_presigned_url(self, method, **kwargs):
        pass

class TestJournalEntriesExport(TestBase(PATHS)):

    def test_good_api_request_with_ledger_ids(self, monkeypatch):
        import boto3
        from app.v1.journal_entries.post.bulk_export import handler

        request = {
            "body": "{ \"ledgerIds\": [\"a92bde1e-7825-429d-aaae-909f2d7a8df1\"] }"
        }

        monkeypatch.setattr(boto3, "client", lambda service: Boto3Mocked())

        result = handler(request, LambdaContext())
        assert 201 == result['statusCode']


    def test_bad_api_request_with_ledger_ids(self):
        import boto3
        from app.v1.journal_entries.post.bulk_export import handler
        request = {
            "body": "{ \"ledgerIds\": [\"a92bde1e-7825-429d-aaae-909f2d7a8df\"] }"
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_good_api_request_with_fund_ids(self, monkeypatch):
        import boto3
        from app.v1.journal_entries.post.bulk_export import handler
        request = {
            "body": "{ \"fundIds\": [\"a92bde1e-7825-429d-aaae-909f2d7a8df1\"] }"
        }

        monkeypatch.setattr(boto3, "client", lambda service: Boto3Mocked())

        result = handler(request, LambdaContext())
        assert 201 == result['statusCode']


    def test_bad_api_request_with_fund_ids(self):
        import boto3
        from app.v1.journal_entries.post.bulk_export import handler
        request = {
            "body": "{ \"fundIds\": [\"a92bde1e-7825-429d-aaae-909f2d7a8df\"] }"
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_missing_id(self):
        from app.v1.journal_entries.post.bulk_export import handler
        request = {
            "body": {
            }
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']


    def test_bad_api_request_with_both_ledger_and_fund_ids(self):
        import boto3
        from app.v1.journal_entries.post.bulk_export import handler
        request = {
            "body": "{ \"ledgerIds\": [\"a92bde1e-7825-429d-aaae-909f2d7a8df\"], \"fundIds\": [\"a92bde1e-7825-429d-aaae-909f2d7a8df\"]}"
        }

        result = handler(request, LambdaContext())

        assert 400 == result['statusCode']
