import aws_cdk as cdk
from constructs import Construct
from pathlib import PurePath

from env import ENV

from shared.base_stack import BaseStack
from shared.utils import get_stack_prefix, QLDB_DIR


from shared.layers import get_qldb_layer, get_pyqldb_layer

from shared.get_cdk import get_vpc, get_subnets, get_replication_vpc, get_replication_subnets

CODE_DIR = str(PurePath(QLDB_DIR, "qldb_tables"))


class LambdaTriggerStack(BaseStack):
    def __init__(self, scope: Construct, id: str, is_replication: bool = False, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ledger_name = ENV["deploy"]["LEDGER_NAME"]

        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)

        if is_replication:
            vpc = get_replication_vpc(self)
            subnets = get_replication_subnets(self)
        else:
            vpc = get_vpc(self)
            subnets = get_subnets(self)

        function = cdk.triggers.TriggerFunction(
            self,
            get_stack_prefix() + "ark-qldb-trigger-lambda",
            function_name=get_stack_prefix() + "ark-qldb-trigger-lambda",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            handler="qldb_tables.handler",
            code=cdk.aws_lambda.Code.from_asset(CODE_DIR),
            timeout=cdk.Duration.seconds(60),
            environment={"LEDGER_NAME": ledger_name},
            layers=[qldb_layer, qldb_reqs],
            vpc=vpc,
            vpc_subnets=cdk.aws_ec2.SubnetSelection(subnets=subnets),
        )

        ledger_arn = (
            "arn:aws:qldb:"
            + kwargs["env"].region
            + ":"
            + kwargs["env"].account
            + ":ledger/"
            + ledger_name
        )

        qldb_send_command_statement = cdk.aws_iam.PolicyStatement(
            actions=["qldb:SendCommand"], resources=[ledger_arn]
        )

        qldb_actions_statement = cdk.aws_iam.PolicyStatement(
            actions=[
                "qldb:ShowCatalog",
                "qldb:PartiQLInsert",
                "qldb:ExecuteStatement",
                "qldb:PartiQLCreateTable",
                "qldb:PartiQLCreateIndex",
                "qldb:PartiQLSelect",
            ],
            resources=[ledger_arn + "/*"],
        )

        qldb_policy = cdk.aws_iam.Policy(
            self,
            get_stack_prefix() + "ark-db-qldb-policy",
            policy_name=get_stack_prefix() + "ark-db-qldb-policy",
            statements=[qldb_send_command_statement, qldb_actions_statement],
        )

        function.role.attach_inline_policy(qldb_policy)
