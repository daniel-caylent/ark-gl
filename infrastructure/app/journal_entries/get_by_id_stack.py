from pathlib import PurePath

from constructs import Construct

from shared.base_stack import BaseStack
from shared.get_cdk import build_lambda_function
from shared.layers import (
    get_models_layer,
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
)
from shared.utils import JOURNAL_ENTRIES_DIR

import aws_cdk as cdk

CODE_DIR = str(PurePath(JOURNAL_ENTRIES_DIR, "get"))
MODELS_DIR = str(PurePath(JOURNAL_ENTRIES_DIR, "shared"))


class JournalEntriesGetByIdStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)

        lambda_function = build_lambda_function(
            self,
            CODE_DIR,
            handler="get_by_id.handler",
            layers=[shared_layer, pymysql_layer, db_layer],
            description="journal entries get by id",
            exclude=["get.py"],
        )

        cdk.CfnOutput(
            self,
            "ark-journal-entries-get-by-id-function-arn",
            value=lambda_function.function_arn,
            export_name=self.STACK_PREFIX
            + "ark-journal-entries-get-by-id-function-arn",
        )
