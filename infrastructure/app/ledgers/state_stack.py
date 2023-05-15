from pathlib import PurePath

import aws_cdk as cdk
from constructs import Construct

from ..base_stack import BaseStack
from ..get_cdk import build_lambda_function
from ..layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
    get_pyqldb_layer,
    get_qldb_layer
)
from ..utils import LEDGERS_DIR


CODE_DIR = str(PurePath(LEDGERS_DIR, 'state'))

class LedgersStateStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)
        pyqldb_layer = get_pyqldb_layer(self)
        qldb_layer = get_qldb_layer(self)

        lambda_function = build_lambda_function(self, CODE_DIR,
            handler="state.handler",
            layers=[shared_layer, pymysql_layer, db_layer, pyqldb_layer, qldb_layer],
            description="ledgers state"
        )

        cdk.CfnOutput(
            self, "ark-ledger-state-function-arn",
            value=lambda_function.function_arn,
            export_name= self.STACK_PREFIX + "ark-ledger-state-function-arn"
        )

