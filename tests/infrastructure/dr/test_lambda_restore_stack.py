import aws_cdk as core
from constructs import Construct
import aws_cdk.assertions as assertions

from .dr_base_test import DrTestBase


class DrFakeStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.mock_bucket = core.aws_s3.Bucket(self, "mock-bucket")
        self.mock_queue = core.aws_sqs.Queue(self, "mock-queue")


class TestLambdaRestoreStack(DrTestBase):
    cdk_env = core.Environment(
        account="131578276461",
        region="us-east-2",
    )

    def test_lambda_restore_stack_created(self):
        from app.dr import LambdaRestoreStack

        app = core.App()
        fake_stack = DrFakeStack(app, "fake-stack", env=self.__class__.cdk_env)
        stack = LambdaRestoreStack(
            app,
            "cdk",
            bucket=fake_stack.mock_bucket,
            queue=fake_stack.mock_queue,
            env=self.__class__.cdk_env,
        )
        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::IAM::Policy", 3)
        template.resource_count_is("AWS::Lambda::Function", 1)
        template.resource_count_is("AWS::IAM::Role", 1)
        template.resource_count_is("AWS::Lambda::EventSourceMapping", 1)
