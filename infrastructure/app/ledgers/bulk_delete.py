from pathlib import PurePath

import aws_cdk as cdk
from constructs import Construct

from shared.base_stack import BaseStack
from shared.get_cdk import build_lambda_function
from shared.layers import get_pymysql_layer, get_shared_layer, get_database_layer
from shared.utils import LEDGERS_DIR


CODE_DIR = str(PurePath(LEDGERS_DIR, "delete"))


class LedgersBulkDeleteStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)

        lambda_function = build_lambda_function(
            self,
            CODE_DIR,
            handler="bulk.handler",
            layers=[shared_layer, pymysql_layer, db_layer],
            description="ledgers bulk delete",
            exclude=["delete*"],
        )

        cdk.CfnOutput(
            self,
            "ark-ledger-bulk-delete-function-arn",
            value=lambda_function.function_arn,
            export_name=self.STACK_PREFIX + "ark-ledger-bulk-delete-function-arn",
        )
