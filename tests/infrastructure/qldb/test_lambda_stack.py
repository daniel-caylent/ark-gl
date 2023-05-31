import aws_cdk as core
import aws_cdk.assertions as assertions

from .qldb_base_test import QldbTestBase


class TestLambdaStack(QldbTestBase):
    cdk_env = core.Environment(
        account="131578276461",
        region="us-east-2",
    )

    def test_lambda_stack_created(self):
        from infrastructure.qldb.lambda_stack import LambdaTriggerStack

        app = core.App()
        stack = LambdaTriggerStack(app, "cdk", env=self.__class__.cdk_env)
        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::IAM::Policy", 1)
        template.resource_count_is("AWS::Lambda::Function", 2)
        template.resource_count_is("AWS::Lambda::LayerVersion", 2)
        template.resource_count_is("AWS::IAM::Role", 2)
