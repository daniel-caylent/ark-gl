from pathlib import PurePath

import aws_cdk as cdk
from constructs import Construct

from shared.utils import get_stack_prefix
from shared.base_stack import BaseStack
from shared.get_cdk import build_decorated_qldb_lambda_function
from shared.layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
    get_qldb_layer,
    get_pyqldb_layer,
)
from shared.utils import RECONCILIATION_DIR
from env import ENV


CODE_DIR = str(PurePath(RECONCILIATION_DIR, "load_balancer"))


class LoadBalancerJournalEntriesStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = get_stack_prefix().lower() + "reconciliation-bucket"

        self.bucket = cdk.aws_s3.Bucket(
            self,
            "ark-je-export-bucket",
            bucket_name=bucket_name,
            encryption=cdk.aws_s3.BucketEncryption.S3_MANAGED,
            block_public_access=cdk.aws_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            versioned=True,
            enforce_ssl=True,
        )
        
        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)
        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)

        self.lambda_function = build_decorated_qldb_lambda_function(
            self,
            CODE_DIR,
            handler="load_balancer.handler",
            layers=[shared_layer, pymysql_layer, db_layer, qldb_layer, qldb_reqs],
            description="load balancer for journal entries in the reconciliation",
            env={
                "sqs_name": self.STACK_PREFIX + ENV["sqs_name"],
                "LOG_LEVEL": "INFO",
                "BUCKET_NAME": bucket_name
            },
            cdk_env=kwargs["env"],
        )
        
        self.bucket.grant_read_write(self.lambda_function.role)