import aws_cdk as cdk
from constructs import Construct

from .base_stack import BaseStack

class QldbStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ledger = cdk.aws_qldb.CfnLedger(
            self, "ark-qldb-ledger",
            permissions_mode="STANDARD",
            kms_key="AWS_OWNED_KMS_KEY",
            name="ARKGL",
            deletion_protection=True
        )

        cdk.CfnOutput(
            self, "qldbLedger",
            value=ledger.name,
            export_name= self.STACK_PREFIX + "qldbLedger"
        )
