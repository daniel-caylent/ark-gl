from pathlib import PurePath

from constructs import Construct

from shared.base_stack import BaseStack
from shared.get_cdk import build_lambda_function
from shared.layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
    get_journal_entries_shared_layer
)
from shared.utils import JOURNAL_ENTRIES_DIR

import aws_cdk as cdk

CODE_DIR = str(PurePath(JOURNAL_ENTRIES_DIR, "get"))


class JournalEntriesGetStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)
        journal_entries_shared_layer = get_journal_entries_shared_layer(self)

        lambda_function = build_lambda_function(
            self,
            CODE_DIR,
            handler="get.handler",
            layers=[shared_layer, pymysql_layer, db_layer, journal_entries_shared_layer],
            description="journal entries get",
            exclude=["get_by_id.py"],
        )

        cdk.CfnOutput(
            self,
            "ark-journal-entries-get-function-arn",
            value=lambda_function.function_arn,
            export_name=self.STACK_PREFIX + "ark-journal-entries-get-function-arn",
        )
