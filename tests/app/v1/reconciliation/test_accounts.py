
from tests.app.data import (
    LambdaContext
)
from tests.utils import APP_SHARED_LAYER
from tests.test_base import TestBase


class TestReconciliationAccounts(TestBase([APP_SHARED_LAYER], env={"AWS_REGION": "us-east-1"})):

    def test_matching_records(self):
        from app.v1.reconciliation.accounts.account import handler

        result = handler(None, LambdaContext())
        assert 200 == result['statusCode']


    def test_missing_aurora(self, monkeypatch):
        from app.v1.reconciliation.accounts.account import handler

        monkeypatch.setattr("arkdb.accounts.select_by_id", lambda *i,**t: None)

        result = handler(None, LambdaContext())
        assert 400 == result['statusCode']


    def test_not_matching(self, monkeypatch):
        from app.v1.reconciliation.accounts.account import handler

        monkeypatch.setattr("arkdb.accounts.select_by_id", lambda *i,**t: {"uuid": None})

        result = handler(None, LambdaContext())
        assert 400 == result['statusCode']

