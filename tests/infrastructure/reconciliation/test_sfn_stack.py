import aws_cdk as core
from constructs import Construct
import aws_cdk.assertions as assertions

from .reconciliation_base_test import ReconciliationTestBase


class FakeStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.mock_f1 = core.aws_lambda.Function(
            self,
            "mock-f1",
            code=core.aws_lambda.Code.from_inline("print('a')"),
            handler="",
            runtime=core.aws_lambda.Runtime.PYTHON_3_9,
        )
        self.mock_f2 = core.aws_lambda.Function(
            self,
            "mock-f2",
            code=core.aws_lambda.Code.from_inline("print('a')"),
            handler="",
            runtime=core.aws_lambda.Runtime.PYTHON_3_9,
        )
        self.mock_f3 = core.aws_lambda.Function(
            self,
            "mock-f3",
            code=core.aws_lambda.Code.from_inline("print('a')"),
            handler="",
            runtime=core.aws_lambda.Runtime.PYTHON_3_9,
        )


class TestSfnStack(ReconciliationTestBase):
    cdk_env = core.Environment(
        account="131578276461",
        region="us-east-2",
    )

    def test_sfn_stack_created(self):
        from infrastructure.app.reconciliation import StepFunctionStack

        app = core.App()
        fake_stack = FakeStack(app, "fake-stack", env=self.__class__.cdk_env)
        stack = StepFunctionStack(
            app,
            "cdk",
            accounts_reconciliation_lambda=fake_stack.mock_f1,
            ledgers_reconciliation_lambda=fake_stack.mock_f2,
            journals_loadbalancer_lambda=fake_stack.mock_f3,
            env=self.__class__.cdk_env,
        )
        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::IAM::Policy", 2)
        template.resource_count_is("AWS::StepFunctions::StateMachine", 1)
        template.resource_count_is("AWS::IAM::Role", 2)
        template.resource_count_is("AWS::Events::Rule", 1)
