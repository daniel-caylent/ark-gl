import aws_cdk as core
from constructs import Construct
import aws_cdk.assertions as assertions

from .reconciliation_base_test import ReconciliationTestBase


class FakeStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.mock_queue = core.aws_sqs.Queue(self, "mock-queue")


class TestJournalEntriesStack(ReconciliationTestBase):
    cdk_env = core.Environment(
        account="131578276461",
        region="us-east-2",
    )

    def test_je_stack_created(self):
        from infrastructure.app.reconciliation import JournalEntriesReconciliationStack

        app = core.App()
        fake_stack = FakeStack(app, "fake-stack", env=self.__class__.cdk_env)
        stack = JournalEntriesReconciliationStack(
            app, "cdk", queue=fake_stack.mock_queue, env=self.__class__.cdk_env
        )
        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::IAM::Policy", 4)
        template.resource_count_is("AWS::Lambda::Function", 1)
        template.resource_count_is("AWS::IAM::Role", 1)
        template.resource_count_is("AWS::Lambda::LayerVersion", 5)
