import aws_cdk as core
import aws_cdk.assertions as assertions

from .accounts_base_test import AccountsTestBase


class TestAccountsUploadStack(AccountsTestBase):

    cdk_env = core.Environment(
        account = '131578276461',
        region = 'us-east-2',
    )


    def test_accounts_upload_stack_created(self):
        from infrastructure.app.accounts import AccountsUploadStack

        app = core.App()
        stack = AccountsUploadStack(app, "cdk", env=self.__class__.cdk_env)
        template = assertions.Template.from_stack(stack)

        template.resource_count_is('AWS::Lambda::LayerVersion', 3)
        template.resource_count_is('AWS::IAM::Policy', 2)
        template.resource_count_is('AWS::Lambda::Function', 1)
        template.resource_count_is('AWS::IAM::Role', 1)
