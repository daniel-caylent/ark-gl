import aws_cdk as core
import aws_cdk.assertions as assertions

from .api_base_test import ApiTestBase


class TestLedgersNestedStack(ApiTestBase):

    cdk_env = core.Environment(
        account = '131578276461',
        region = 'us-east-2',
    )


    def test_ledgers_nested_stack_created(self):
        from infrastructure.app.api.api_ledgers_stack import LedgersStack

        app = core.App()

        stack = LedgersStack(app, "cdk", "1", "2", env=self.__class__.cdk_env)

        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::CloudFormation::Stack", 1)
