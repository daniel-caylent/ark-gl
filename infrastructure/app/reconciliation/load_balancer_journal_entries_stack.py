from pathlib import PurePath

from constructs import Construct

from ..base_stack import BaseStack

from ..get_cdk import build_qldb_lambda_function, build_decorated_qldb_lambda_function
from ..layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
    get_qldb_layer,
    get_pyqldb_layer,
)
from ..utils import RECONCILIATION_DIR
from env import ENV
import aws_cdk as cdk


CODE_DIR = str(PurePath(RECONCILIATION_DIR, "load_balancer"))


class LoadBalancerJournalEntriesStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)
        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)
        sns_name = self.STACK_PREFIX + ENV["sns_name"]
        lambda_function = build_decorated_qldb_lambda_function(
            self,
            CODE_DIR,
            handler="load_balancer.handler",
            layers=[pymysql_layer, db_layer, qldb_layer, qldb_reqs],
            description="load balancer for journal entries in the reconciliation",
            env={
                "sqs_name": self.STACK_PREFIX + ENV["sqs_name"],
                "sns_name": sns_name,
                "sns_arn": "arn:aws:sns:"
                + self.region
                + ":"
                + self.account
                + ":"
                + sns_name,
            },
        )
