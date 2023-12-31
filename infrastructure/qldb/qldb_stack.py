import aws_cdk as cdk
from constructs import Construct

from shared.base_stack import BaseStack
from env import ENV


class QldbStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ledger_name = ENV["deploy"]["LEDGER_NAME"]

        ledger = cdk.aws_qldb.CfnLedger(
            self,
            "ark-qldb-ledger",
            permissions_mode="STANDARD",
            kms_key="AWS_OWNED_KMS_KEY",
            name=ledger_name,
            deletion_protection=True,
        )

        cdk.CfnOutput(
            self,
            "qldbLedger",
            value=ledger.name,
            export_name=self.STACK_PREFIX + "qldbLedger",
        )
