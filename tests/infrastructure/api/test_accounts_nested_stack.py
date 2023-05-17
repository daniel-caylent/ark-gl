import aws_cdk as core
from constructs import Construct
import aws_cdk.assertions as assertions

from .api_base_test import ApiTestBase


class AccountsFakeStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        from infrastructure.app.api.api_account_nested_stack import AccountNestedStack
        super().__init__(scope, id, **kwargs)

        AccountNestedStack(
            self,
            "ark-gl-accounts-api-nested",
            "1",
            "2")


class TestAccountsNestedStack(ApiTestBase):

    cdk_env = core.Environment(
        account = '131578276461',
        region = 'us-east-2',
    )

    def test_accounts_nested_stack_created(self):
        app = core.App()

        stack = AccountsFakeStack(app, "cdk", env=self.__class__.cdk_env)

        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::CloudFormation::Stack", 1)
