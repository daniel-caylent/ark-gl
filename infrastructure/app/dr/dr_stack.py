import aws_cdk as cdk
from constructs import Construct
from pathlib import PurePath
import sys
import os
from aws_cdk import aws_s3 as s3
from ..get_cdk import build_dr_lambda_function
from ..layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
    get_qldb_layer,
    get_pyqldb_layer,
)
# setting path
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from app.base_stack import BaseStack
from app.utils import get_stack_prefix

# sys.path.append('../')
from env import ENV
from ..utils import DR_DIR
CODE_DIR = str(PurePath(DR_DIR, "export"))
class DRStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        dr_bucket_name = ENV["dr_bucket_name"]
        ledger_name = ENV["ledger_name"] 
        source_bucket = s3.Bucket(
            self,
            "ark-dr-bucket",
            bucket_name=dr_bucket_name,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            enforce_ssl=True
        )

        shared_layer = get_shared_layer(self)
        #pymysql_layer = get_pymysql_layer(self)
        #db_layer = get_database_layer(self)
        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)

        self.lambda_function = build_dr_lambda_function(
            self,
            CODE_DIR,
            handler="export_qldb.handler",
            layers=[shared_layer, qldb_layer, qldb_reqs],
            description="dr qldb export lambda",
            env={
                "dr_bucket": dr_bucket_name,
                "ledger_name": ledger_name,
                "region": self.region,
                "LOG_LEVEL": "INFO",
            },
        )
        # Create the destination bucket in the replica region
        #replica_region = 'us-west-2'  # Replace with your desired replica region
        #replica_bucket_name = 'arkgl-dr-replica'
        #replica_bucket = s3.Bucket(
        #    self,
        #    'arkgl-dr-replica-bucket',
        #    bucket_name=replica_bucket_name,
        #    encryption=s3.BucketEncryption.S3_MANAGED,
        #    block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        #    versioned=True,
        #    enforce_ssl=True,
        #    bucket_key_enabled=True,
        #    replication_destinations=[
        #        s3.ReplicationDestination(
        #            bucket=source_bucket,
        #            region=replica_region
        #        )
        #    ]
        #)

        # Enable compliance mode for the replica bucket
        #replica_bucket.enable_compliance_mode()
