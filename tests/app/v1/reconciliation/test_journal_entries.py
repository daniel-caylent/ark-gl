
from tests.app.data import (
    LambdaContext
)
from tests.utils import APP_SHARED_LAYER
from tests.test_base import TestBase



class TestReconciliationJournalEntries(TestBase([APP_SHARED_LAYER], env={"AWS_REGION": "us-east-1"})):

    def test_matching_records(self):
        from app.v1.reconciliation.journal_entries.journal_entry import handler
        event = {
            "Records": [
                {
                    "body": "uuid1,uuid2"
                }
            ]
        }
        result = handler(event, LambdaContext())
        assert 200 == result['statusCode']


    def test_missing_aurora(self, monkeypatch):
        from app.v1.reconciliation.journal_entries.journal_entry import handler

        monkeypatch.setattr("arkdb.journal_entries.select_by_id", lambda *i,**t: None)
        event = {
            "Records": [
                {
                    "body": "uuid1,uuid2"
                }
            ]
        }
        result = handler(event, LambdaContext())
        assert 400 == result['statusCode']


    def test_not_matching(self, monkeypatch):
        from app.v1.reconciliation.journal_entries.journal_entry import handler

        monkeypatch.setattr("arkdb.journal_entries.select_by_id", lambda *i,**t: {"uuid": None})
        event = {
            "Records": [
                {
                    "body": "uuid1,uuid2"
                }
            ]
        }

        result = handler(event, LambdaContext())
        assert 400 == result['statusCode']

