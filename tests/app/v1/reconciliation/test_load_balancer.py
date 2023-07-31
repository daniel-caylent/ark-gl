
from tests.app.data import (
    LambdaContext
)
from tests.utils import APP_SHARED_LAYER
from tests.test_base import TestBase

class Boto3Mocked:

    def get_queue_url(self, **kwargs):
        return {
            "QueueUrl": "url"
        }
  
    def send_message(
            self,
            QueueUrl=None,
            MessageBody=None
    ):
        return None

env = {
    "sqs_name": "test",
}

class TestReconciliationLoadBalancer(TestBase([APP_SHARED_LAYER], env=env)):

    def test_good_api_request_with_ledger_ids(self, monkeypatch):
        import boto3
        from app.v1.reconciliation.load_balancer.load_balancer import handler

        monkeypatch.setattr(boto3, "client", lambda service: Boto3Mocked())

        result = handler(None, LambdaContext())
        assert 200 == result['statusCode']

