import json
import sys

from tests.app.data import (
    LambdaContext
)
from tests.utils import APP_SHARED_LAYER, MOCK_DIR
from tests.test_base import TestBase

env = {
    "AWS_REGION": "test",
    "LEDGER_NAME": "test"
}
class TestDrRestore(TestBase([APP_SHARED_LAYER, MOCK_DIR], env=env)):

    def test_good_api_request_with_ledger_ids(self, monkeypatch):
        from app.v1.dr.restore.restore_qldb import handler

        event = {
            "Records": [
                {"body": "PATH"}
            ]
        }
        result = handler(event, LambdaContext())
        assert 200 == result['statusCode']
