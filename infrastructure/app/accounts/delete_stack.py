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
from ..utils import ACCOUNTS_DIR

import aws_cdk as cdk

CODE_DIR = str(PurePath(ACCOUNTS_DIR, 'delete'))
MODELS_DIR = str(PurePath(ACCOUNTS_DIR, 'models'))

class AccountsDeleteStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        models_layer = get_models_layer(self, MODELS_DIR)
        db_layer = get_database_layer(self)

        lambda_function = build_lambda_function(self, CODE_DIR,
            handler="delete.handler",
            layers=[shared_layer, pymysql_layer, models_layer, db_layer],
            description="delete account by id"
        )

        cdk.CfnOutput(
            self, "ark-account-delete-function-arn",
            value=lambda_function.function_arn,
            export_name= self.STACK_PREFIX + "ark-account-delete-function-arn"
        )
