import aws_cdk as core
import aws_cdk.assertions as assertions

from .api_base_test import ApiTestBase


class TestAccountAttributesNestedStack(ApiTestBase):

    cdk_env = core.Environment(
        account = '131578276461',
        region = 'us-east-2',
    )

    def test_account_attributes_stack_created(self):
        from infrastructure.app.api.api_account_attribute_stack import AccountAttributesStack

        app = core.App()

        stack = AccountAttributesStack(app, "cdk", "1", "2", env=self.__class__.cdk_env)

        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::ApiGateway::Resource", 1)
        template.resource_count_is("AWS::ApiGateway::Method", 1)
        template.resource_count_is("AWS::IAM::Role", 1)
        template.resource_count_is("AWS::IAM::Policy", 1)
