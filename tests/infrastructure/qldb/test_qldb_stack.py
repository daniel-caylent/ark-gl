import aws_cdk as core
import aws_cdk.assertions as assertions

from .qldb_base_test import QldbTestBase


class TestQldbStack(QldbTestBase):
    cdk_env = core.Environment(
        account="131578276461",
        region="us-east-2",
    )

    def test_qldb_stack_created(self):
        from infrastructure.qldb.qldb_stack import QldbStack

        app = core.App()
        stack = QldbStack(app, "cdk", env=self.__class__.cdk_env)
        template = assertions.Template.from_stack(stack)

        template.resource_count_is("AWS::QLDB::Ledger", 1)
