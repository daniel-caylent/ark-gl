from pathlib import PurePath

from constructs import Construct

from shared.base_stack import BaseStack
from shared.get_cdk import build_qldb_lambda_function
from shared.layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
    get_qldb_layer,
    get_pyqldb_layer,
)
from shared.utils import JOURNAL_ENTRIES_DIR

import aws_cdk as cdk

CODE_DIR = str(PurePath(JOURNAL_ENTRIES_DIR, "put"))


class JournalEntriesStateStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)
        qldb_layer = get_qldb_layer(self)
        pyqldb_layer = get_pyqldb_layer(self)

        lambda_function = build_qldb_lambda_function(
            self,
            CODE_DIR,
            handler="state.handler",
            layers=[shared_layer, pymysql_layer, db_layer, qldb_layer, pyqldb_layer],
            description="journal entries state",
            cdk_env=kwargs["env"],
            exclude=["put.py", "models.py"]
        )

        cdk.CfnOutput(
            self,
            "ark-journal-entries-state-function-arn",
            value=lambda_function.function_arn,
            export_name=self.STACK_PREFIX + "ark-journal-entries-state-function-arn",
        )
