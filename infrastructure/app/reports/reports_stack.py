from pathlib import PurePath

from constructs import Construct

from shared.base_stack import BaseStack
from shared.get_cdk import build_lambda_function
from shared.layers import get_pymysql_layer, get_shared_layer, get_database_layer
from shared.utils import REPORTS_DIR

import aws_cdk as cdk

CODE_DIR = str(PurePath(REPORTS_DIR))


class ReportsStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)

        trial_balance = build_lambda_function(
            self,
            CODE_DIR,
            handler="trial_balance.handler",
            name="trial-balance",
            layers=[shared_layer, pymysql_layer, db_layer],
            description="trial balance report",
        )

        trial_balance_detail = build_lambda_function(
            self,
            CODE_DIR,
            handler="trial_balance_detail.handler",
            name="trial-balance-detail",
            layers=[shared_layer, pymysql_layer, db_layer],
            description="trial balance detail report",
        )

        cdk.CfnOutput(
            self,
            "ark-reports-trial-balance-function-arn",
            value=trial_balance.function_arn,
            export_name=self.STACK_PREFIX + "ark-reports-trial-balance-function-arn",
        )

        cdk.CfnOutput(
            self,
            "ark-reports-trial-balance-detail-function-arn",
            value=trial_balance_detail.function_arn,
            export_name=self.STACK_PREFIX + "ark-reports-trial-balance-detail-function-arn",
        )
