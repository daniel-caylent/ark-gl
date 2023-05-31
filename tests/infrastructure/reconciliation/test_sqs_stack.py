import aws_cdk as core
from constructs import Construct
import aws_cdk.assertions as assertions

from .reconciliation_base_test import ReconciliationTestBase


class TestSqsStack(ReconciliationTestBase):
    cdk_env = core.Environment(
        account="131578276461",
        region="us-east-2",
    )

    def test_sfn_stack_created(self):
        from infrastructure.app.reconciliation import SQSStack

        app = core.App()
        stack = SQSStack(app, "cdk", env=self.__class__.cdk_env)
        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::SQS::Queue", 1)
