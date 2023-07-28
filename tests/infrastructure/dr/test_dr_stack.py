import aws_cdk as core
import aws_cdk.assertions as assertions

from .dr_base_test import DrTestBase


class TestDrStack(DrTestBase):
    cdk_env = core.Environment(
        account="131578276461",
        region="us-east-2",
    )

    def test_dr_stack_created(self):
        from infrastructure.app.dr import DRStack

        app = core.App()
        stack = DRStack(app, "cdk", env=self.__class__.cdk_env)
        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::S3::Bucket", 1)
        template.resource_count_is("AWS::IAM::Policy", 4)
        template.resource_count_is("AWS::Lambda::Function", 1)
        template.resource_count_is("AWS::IAM::Role", 2)
        template.resource_count_is("AWS::Events::Rule", 1)
