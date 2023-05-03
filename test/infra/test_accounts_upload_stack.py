import aws_cdk as core
import aws_cdk.assertions as assertions
from infrastructure.app.accounts import AccountsUploadStack

import unittest


class TestAccountsUploadStack(unittest.TestCase):

    cdk_env = core.Environment(
        account = '131578276461',
        region = 'us-east-2',
    )


    def test_accounts_upload_stack_created(self):
        app = core.App()
        stack = AccountsUploadStack(app, "cdk", env=self.__class__.cdk_env)
        template = assertions.Template.from_stack(stack)

        template.resource_count_is('AWS::Lambda::LayerVersion', 5)
        template.resource_count_is('AWS::IAM::Policy', 2)
        template.resource_count_is('AWS::Lambda::Function', 1)
        template.resource_count_is('AWS::IAM::Role', 1)


if __name__ == "__main__":
    unittest.main()
