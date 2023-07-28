
from tests.app.data import (
    LambdaContext
)
from tests.utils import APP_SHARED_LAYER
from tests.test_base import TestBase

class SessionMocked:
    def client(self, arg):
      return ClientMocked()

class ClientMocked:
    def export_journal_to_s3(
        self,
        Name=None,
        S3ExportConfiguration=None,
        InclusiveStartTime=None,
        ExclusiveEndTime=None,
        RoleArn=None,
        OutputFormat=None):

        return {
            "ExportId": "1"
        }


env = {
    "DR_BUCKET_NAME": "test",
    "LEDGER_NAME": "test",
    "AWS_REGION": "test",
    "ROLE_ARN": "test",
    "QLDB_EXPORT_TRIGGER_HOUR": 1
}

class TestDrExport(TestBase([APP_SHARED_LAYER], env=env)):

    def test_good_export(self, monkeypatch):
        import boto3
        from app.v1.dr.export.export_qldb import handler

        monkeypatch.setattr(boto3, "Session", lambda region_name=None: SessionMocked())

        result = handler(None, LambdaContext())
        assert 200 == result['statusCode']

