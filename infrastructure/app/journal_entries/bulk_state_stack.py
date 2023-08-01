from pathlib import PurePath

import aws_cdk as cdk
from constructs import Construct

from shared.base_stack import BaseStack
from shared.get_cdk import build_lambda_function
from shared.layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer,
    get_qldb_layer,
    get_pyqldb_layer,
    get_journal_entries_shared_layer
)
from shared.utils import JOURNAL_ENTRIES_DIR, get_stack_prefix

from env import ENV

CODE_DIR = str(PurePath(JOURNAL_ENTRIES_DIR, "put"))


class JournalEntriesBulkStateStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = get_stack_prefix() + ENV['JOURNAL_ENTRIES_BULK_STATE_BUCKET_NAME']

        self.bucket = cdk.aws_s3.Bucket(
            self,
            "ark-journal-entries-bulk-state-bucket",
            bucket_name=bucket_name,
            encryption=cdk.aws_s3.BucketEncryption.S3_MANAGED,
            block_public_access=cdk.aws_s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            enforce_ssl=True,
        )

        je_bulk_state_actions_statement = cdk.aws_iam.PolicyStatement(
            actions=[
                "s3:*",
            ],
            resources=[
                self.bucket.bucket_arn,
                self.bucket.bucket_arn + "/*",
            ],
        )

        je_bucket_policy = cdk.aws_iam.Policy(
            self,
            "ark-journal-entries-bulk-state-bucket-policy",
            policy_name="ark-journal-entries-bulk-state-bucket-policy",
            statements=[je_bulk_state_actions_statement],
        )

        dead_letter_queue = cdk.aws_sqs.Queue(
            self,
            "ark-sqs-journal-entries-bulk-state-process-dl",
            queue_name=self.STACK_PREFIX + ENV["SQS_JOURNAL_ENTRY_BULK_STATE_PROCESS_DL"],
        )

        queue = cdk.aws_sqs.Queue(
            self,
            id="ark-sqs-journal-entries-bulk-state-process",
            queue_name=self.STACK_PREFIX + ENV["SQS_JOURNAL_ENTRY_BULK_STATE_PROCESS"],
            visibility_timeout=cdk.Duration.seconds(60),
            dead_letter_queue=cdk.aws_sqs.DeadLetterQueue(
                max_receive_count=3,
                queue=dead_letter_queue
            )
        )

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        db_layer = get_database_layer(self)
        journal_entries_shared_layer = get_journal_entries_shared_layer(self)

        lambda_function_state_db = build_lambda_function(
            self,
            CODE_DIR,
            handler="bulk_state_db.handler",
            layers=[shared_layer, pymysql_layer, db_layer, journal_entries_shared_layer],
            description="journal entries bulk state db",
            name="bulk_state_db",
            exclude=["update*", "state*", "put*", "bulk_state_qldb*"],
            env={
                "JOURNAL_ENTRIES_BULK_STATE_BUCKET_NAME": bucket_name,
                "SQS_QUEUE_URL": queue.queue_url,
                "LOG_LEVEL": "INFO",
            },
        )

        sqs_actions_statement = cdk.aws_iam.PolicyStatement(
            actions=[
                "sqs:SendMessage",
            ],
            resources=[queue.queue_arn],
        )

        state_policy = cdk.aws_iam.Policy(
            self,
            "ark-bulk-state-policy",
            policy_name=self.STACK_PREFIX+"ark-bulk-state-policy",
            statements=[
                sqs_actions_statement,
            ],
        )

        lambda_function_state_db.role.attach_inline_policy(state_policy)
        lambda_function_state_db.role.attach_inline_policy(je_bucket_policy)

        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)

        lambda_function_state_qldb = build_lambda_function(
            self,
            CODE_DIR,
            handler="bulk_state_qldb.handler",
            layers=[shared_layer, qldb_layer, qldb_reqs],
            name="bulk_state_qldb",
            description="journal entries bulk state qldb",
            exclude=["update*", "state*", "put*", "bulk_state_db*"],
            env={
                "JOURNAL_ENTRIES_BULK_STATE_BUCKET_NAME": bucket_name,
                "LOG_LEVEL": "INFO",
            }
        )

        event_source = cdk.aws_lambda_event_sources.SqsEventSource(
            queue=queue,
            batch_size=1,
            enabled=True
        )

        lambda_function_state_qldb.add_event_source(event_source)
        lambda_function_state_qldb.role.attach_inline_policy(je_bucket_policy)

        ledger_name = ENV["deploy"]["LEDGER_NAME"]

        ledger_arn = (
            "arn:aws:qldb:"
            + kwargs["env"].region
            + ":"
            + kwargs["env"].account
            + ":ledger/"
            + ledger_name
        )

        qldb_send_command_statement = cdk.aws_iam.PolicyStatement(
            actions=["qldb:SendCommand"], resources=[ledger_arn]
        )

        qldb_actions_statement = cdk.aws_iam.PolicyStatement(
            actions=[
                "qldb:ShowCatalog",
                "qldb:PartiQLInsert",
                "qldb:ExecuteStatement",
                "qldb:PartiQLSelect",
            ],
            resources=[ledger_arn + "/*"],
        )

        qldb_policy = cdk.aws_iam.Policy(
            self,
            get_stack_prefix() + "ark-db-journal-entries-bulk-state-qldb-policy",
            policy_name=get_stack_prefix() + "ark-db-journal-entries-bulk-state-qldb",
            statements=[qldb_send_command_statement, qldb_actions_statement],
        )

        lambda_function_state_qldb.role.attach_inline_policy(qldb_policy)

        cdk.CfnOutput(
            self,
            "ark-journal-entries-bulk-state-function-arn",
            value=lambda_function_state_db.function_arn,
            export_name=self.STACK_PREFIX + "ark-journal-entries-bulk-state-function-arn",
        )
