import aws_cdk as cdk
from constructs import Construct
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
parent_2 = os.path.dirname(parent)
sys.path.append(parent_2)
from infrastructure.app.base_stack import BaseStack
from env import ENV

class QldbStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ledger_name = ENV["ledger_name"]

        ledger = cdk.aws_qldb.CfnLedger(
            self, "ark-qldb-ledger",
            permissions_mode="STANDARD",
            kms_key="AWS_OWNED_KMS_KEY",
            name=ledger_name,
            deletion_protection=True
        )

        cdk.CfnOutput(
            self, "qldbLedger",
            value=ledger.name,
            export_name= self.STACK_PREFIX + "qldbLedger"
        )
