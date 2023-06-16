import aws_cdk as core
import aws_cdk.assertions as assertions

from .reconciliation_base_test import ReconciliationTestBase


class TestLedgersReconciliationStack(ReconciliationTestBase):
    cdk_env = core.Environment(
        account="131578276461",
        region="us-east-2",
    )

    def test_ledgers_reconciliation_stack_created(self):
        from infrastructure.app.reconciliation import LedgersReconciliationStack

        app = core.App()
        stack = LedgersReconciliationStack(app, "cdk", env=self.__class__.cdk_env)
        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::IAM::Policy", 4)
        template.resource_count_is("AWS::Lambda::Function", 1)
        template.resource_count_is("AWS::IAM::Role", 1)
        template.resource_count_is("AWS::Lambda::LayerVersion", 5)
