from pathlib import PurePath

from constructs import Construct

from shared.base_stack import BaseStack
from shared.get_cdk import (
    build_lambda_function,
    build_integration_responses,
    build_method_response,
    build_lambda_integration,
)
from shared.layers import (
    get_shared_layer,
    get_pymysql_layer,
    get_database_layer
)
from shared.utils import ACCOUNTS_ATTR_DIR

import aws_cdk as cdk

CODE_DIR = str(PurePath(ACCOUNTS_ATTR_DIR, "get"))


class AccountAttributesGetStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)

        lambda_function = build_lambda_function(
            self,
            CODE_DIR,
            "get.handler",
            layers=[shared_layer, pymysql_layer, db_layer],
            description="account attributes get"
        )

        cdk.CfnOutput(
            self,
            "ark-account-attribute-get-function-arn",
            value=lambda_function.function_arn,
            export_name=self.STACK_PREFIX + "ark-account-attribute-get-function-arn",
        )
