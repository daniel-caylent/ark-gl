
from tests.app.data import (
    LambdaContext
)
from tests.utils import APP_SHARED_LAYER
from tests.test_base import TestBase

class Boto3Mocked:

    def put_object(self, **kwargs):
        pass

    def generate_presigned_url(self, method, **kwargs):
        pass
    
    def get_paginator(self, arg):
        return PaginatorMocked()
    
    def send_message(self, QueueUrl=None, MessageBody=None):
        return None


class PaginatorMocked:
    
    def paginate(self, Bucket=None):
        return [
            {"Contents": [
                {"Key": "test.json"}
            ]}
        ]

env = {
    "DR_BUCKET_NAME": "test",
    "SQS_QUEUE_URL": "test"
}

class TestDrDistribute(TestBase([APP_SHARED_LAYER], env=env)):

    def test_good_api_request_with_ledger_ids(self, monkeypatch):
        import boto3
        from app.v1.dr.distribute.distribute_export import handler

        monkeypatch.setattr(boto3, "client", lambda service: Boto3Mocked())

        result = handler(None, LambdaContext())
        assert 200 == result['statusCode']

