import aws_cdk as cdk
from constructs import Construct
from pathlib import PurePath
import sys
import os
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from ..get_cdk import build_dr_lambda_function, build_qldb_lambda_function, get_vpc
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

EXPORT_CODE_DIR = str(PurePath(DR_DIR, "export"))


class DRStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        cron_hour = ENV["QLDB_EXPORT_TRIGGER_HOUR"]
        vpc = get_vpc(self)
        dr_bucket_name = get_stack_prefix() + ENV["DR_BUCKET_NAME"]
        ledger_name = ENV["ledger_name"]
        self.source_bucket = s3.Bucket(
            self,
            "ark-dr-bucket",
            bucket_name= dr_bucket_name,
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
            resources=[self.source_bucket.bucket_arn, self.source_bucket.bucket_arn+"/*"],
        )

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
            EXPORT_CODE_DIR,
            handler="export_qldb.handler",
            layers=[shared_layer, qldb_layer, qldb_reqs],
            description="dr qldb export lambda",
            env={
                "ROLE_ARN": qldb_role.role_arn,
                "DR_BUCKET_NAME": dr_bucket_name,
                "QLDB_EXPORT_TRIGGER_HOUR": cron_hour, 
                "LOG_LEVEL": "INFO",
            },
            vpc=vpc
        )

        self.lambda_function.role.attach_inline_policy(dr_policy)

        eventbridge_cron = cdk.aws_events.Rule(
            self,
            get_stack_prefix() + "ark-qldb-export-trigger",
            schedule=cdk.aws_events.Schedule.cron(minute=str(0), hour="*/"+str(cron_hour)),
            rule_name=get_stack_prefix() + "ark-qldb-export-trigger",
        )

        # Add statemachine to CW Event Rule
        eventbridge_cron.add_target(
            cdk.aws_events_targets.LambdaFunction(self.lambda_function)
        )

        queue = cdk.aws_sqs.Queue(
            self,
            id="ark-sqs-dr-recovery-process",
            queue_name=self.STACK_PREFIX + ENV["SQS_RECOVERY_PROCESS"],
        )

        self.lambda_function_2 = build_dr_lambda_function(
            self,
            EXPORT_CODE_DIR,
            handler="distribute_export.handler",
            layers=[shared_layer, qldb_layer, qldb_reqs],
            description="dr qldb export lambda",
            env={
                "ROLE_ARN": qldb_role.role_arn,
                "DR_BUCKET_NAME": dr_bucket_name,
                "SQS_QUEUE_URL": queue.queue_url, 
                "LOG_LEVEL": "INFO",
            },
            vpc=vpc
        )
        # Create the destination bucket in the replica region
        # replica_region = 'us-east-2'  # Replace with your desired replica region
        # replica_bucket_name = get_stack_prefix() + 'arkgl-dr-replica'
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
        #            region=replica_region,
        #        )
        #    ]
        # )

        # Enable compliance mode for the replica bucket
        # replica_bucket.enable_compliance_mode()
