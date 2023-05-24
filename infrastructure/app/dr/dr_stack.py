import aws_cdk as cdk
from constructs import Construct
from pathlib import PurePath
import sys
import os
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
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
            enforce_ssl=True,
        )

        qldb_role = iam.Role(
            self,
            "dr-qldb-export-Role",
            assumed_by=iam.ServicePrincipal("qldb.amazonaws.com"),
            description="Example role...",
        )

        dr_actions_statement = cdk.aws_iam.PolicyStatement(
            actions=[
                "s3:*",
            ],
            resources=[source_bucket.bucket_arn, source_bucket.bucket_arn+"/*"],
        )

        ledger_name = ENV["ledger_name"]
        ledger_arn = (
            "arn:aws:qldb:"
            + self.region
            + ":"
            + self.account
            + ":ledger/"
            + ledger_name
        )

        dr_actions_statement2 = cdk.aws_iam.PolicyStatement(
            actions=[
                "qldb:ListJournalS3Exports",
                "qldb:ListJournalS3ExportsForLedger",
                "qldb:ExportJournalToS3",
            ],
            resources=[ledger_arn],
        )

        dr_policy = cdk.aws_iam.Policy(
            self,
            "ark-dr-export-policy",
            policy_name="ark-dr-export-policy",
            statements=[dr_actions_statement, dr_actions_statement2],
        )
        
        qldb_role.attach_inline_policy(dr_policy)
        shared_layer = get_shared_layer(self)
        # pymysql_layer = get_pymysql_layer(self)
        # db_layer = get_database_layer(self)
        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)

        self.lambda_function = build_dr_lambda_function(
            self,
            CODE_DIR,
            handler="export_qldb.handler",
            layers=[shared_layer, qldb_layer, qldb_reqs],
            description="dr qldb export lambda",
            env={
                "role_arn": qldb_role.role_arn,
                "dr_bucket_name": dr_bucket_name,
                "ledger_name": ledger_name,
                "region": self.region,
                "LOG_LEVEL": "INFO",
            },
        )

        self.lambda_function.role.attach_inline_policy(dr_policy)

        # Create the destination bucket in the replica region
        # replica_region = 'us-west-2'  # Replace with your desired replica region
        # replica_bucket_name = 'arkgl-dr-replica'
        # replica_bucket = s3.Bucket(
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
        # )

        # Enable compliance mode for the replica bucket
        # replica_bucket.enable_compliance_mode()
