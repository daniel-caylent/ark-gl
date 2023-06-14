import pytest
import aws_cdk as core
from constructs import Construct
import aws_cdk.assertions as assertions

from .api_base_test import ApiTestBase


class AccountAttributesFakeStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        from infrastructure.app.api.api_account_attribute_nested_stack import AccountAttributesNestedStack
        super().__init__(scope, id, **kwargs)

        AccountAttributesNestedStack(
            self,
            "ark-gl-account-attributes-api-nested",
            "1",
            "2")


class TestAccountAttributesNestedStack(ApiTestBase):

    cdk_env = core.Environment(
        account = '131578276461',
        region = 'us-east-2',
    )

    import pytest
    @pytest.mark.skip(reason="CHECK THIS TEST")
    def test_account_attributes_nested_stack_created(self):
        app = core.App()

        stack = AccountAttributesFakeStack(app, "cdk", env=self.__class__.cdk_env)

        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::CloudFormation::Stack", 1)
