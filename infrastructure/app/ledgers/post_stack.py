from pathlib import PurePath

from constructs import Construct

from ..base_stack import BaseStack
from ..get_cdk import build_lambda_function
from ..layers import (
    get_models_layer,
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer
)
from ..utils import LEDGERS_DIR

import aws_cdk as cdk


CODE_DIR = str(PurePath(LEDGERS_DIR, 'post'))
SHARED_DIR = str(PurePath(LEDGERS_DIR, 'ledgers'))

class LedgersPostStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        ledger_layer = get_models_layer(self, SHARED_DIR)
        db_layer = get_database_layer(self)

        lambda_function = build_lambda_function(self, CODE_DIR,
            handler="post.handler",
            layers=[shared_layer, pymysql_layer, ledger_layer, db_layer],
            description="ledgers post"
        )

        cdk.CfnOutput(
            self, "ark-ledger-post-function-arn",
            value=lambda_function.function_arn,
            export_name= self.STACK_PREFIX + "ark-ledger-post-function-arn"
        )
