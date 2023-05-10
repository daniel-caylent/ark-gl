from pathlib import PurePath

from constructs import Construct

from ..base_stack import BaseStack

from ..get_cdk import build_lambda_function
from ..layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
    get_qldb_layer,
    get_pyqldb_layer
)
from ..utils import ACCOUNTS_DIR

import aws_cdk as cdk


CODE_DIR = str(PurePath(ACCOUNTS_DIR, 'state'))

class AccountsStateStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)
        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)

        lambda_function = build_lambda_function(self, CODE_DIR,
            handler="put.handler",
            layers=[shared_layer, pymysql_layer, db_layer, qldb_layer, qldb_reqs],
            description="accounts state"
        )

        cdk.CfnOutput(
            self, "ark-account-state-function-arn",
            value=lambda_function.function_arn,
            export_name= self.STACK_PREFIX + "ark-account-state-function-arn"
        )
