from pathlib import PurePath
from constructs import Construct

from shared.base_stack import BaseStack
from shared.get_cdk import build_lambda_function
from shared.layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
)
from shared.utils import get_stack_prefix, JOURNAL_ENTRIES_DIR

from env import ENV

import aws_cdk as cdk

CODE_DIR = str(PurePath(JOURNAL_ENTRIES_DIR, "post"))

class JournalEntriesExportStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        export_bucket_name = get_stack_prefix() + ENV["EXPORT_BUCKET_NAME"]

        self.source_bucket = cdk.aws_s3.Bucket(
            self,
            "ark-je-export-bucket",
            bucket_name=export_bucket_name,
            encryption=cdk.aws_s3.BucketEncryption.S3_MANAGED,
            block_public_access=cdk.aws_s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            enforce_ssl=True,
        )

        export_actions_statement = cdk.aws_iam.PolicyStatement(
            actions=[
                "s3:*",
            ],
            resources=[
                self.source_bucket.bucket_arn,
                self.source_bucket.bucket_arn + "/*",
            ],
        )

        export_policy = cdk.aws_iam.Policy(
            self,
            "ark-je-export-policy",
            policy_name="ark-je-export-policy",
            statements=[export_actions_statement],
        )

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)

        lambda_function = build_lambda_function(
            self,
            CODE_DIR,
            handler="export.handler",
            layers=[shared_layer, pymysql_layer, db_layer],
            description="journal entries export",
            exclude=["get*"],
            env={
                "EXPORT_BUCKET_NAME": export_bucket_name,
                "LOG_LEVEL": "INFO",
            },
        )

        lambda_function.role.attach_inline_policy(export_policy)

        cdk.CfnOutput(
            self,
            "ark-journal-entries-export-function-arn",
            value=lambda_function.function_arn,
            export_name=self.STACK_PREFIX + "ark-journal-entries-export-function-arn",
        )
