from pathlib import PurePath

from constructs import Construct

from ..base_stack import BaseStack
from ..get_cdk import build_lambda_function
from ..layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
)
from ..utils import JOURNAL_ENTRIES_DIR

import aws_cdk as cdk

CODE_DIR = str(PurePath(JOURNAL_ENTRIES_DIR, "put"))


class JournalEntriesPutStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)

        lambda_function = build_lambda_function(
            self,
            CODE_DIR,
            handler="put.handler",
            layers=[shared_layer, pymysql_layer, db_layer],
            description="journal entries put"
        )

        cdk.CfnOutput(
            self,
            "ark-journal-entries-put-function-arn",
            value=lambda_function.function_arn,
            export_name=self.STACK_PREFIX
            + "ark-journal-entries-put-function-arn",
        )
