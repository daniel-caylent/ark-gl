import aws_cdk as cdk
from constructs import Construct
from pathlib import PurePath

from shared.get_cdk import build_qldb_lambda_function, build_lambda_function
from shared.layers import (
    get_shared_layer,
    get_qldb_layer,
    get_pyqldb_layer,
    get_awswrangler_layer,
)

from shared.base_stack import BaseStack
from shared.utils import DR_DIR

from env import ENV

RESTORE_CODE_DIR = str(PurePath(DR_DIR, "restore"))
DISTRIBUTE_CODE_DIR = str(PurePath(DR_DIR, "distribute"))


class LambdaRestoreStack(BaseStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        bucket: cdk.aws_s3.Bucket,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        replica_conf = ENV.get("replication_configuration")
        replica_region = replica_conf.get("region")
        ledger_name = ENV["deploy"]["LEDGER_NAME"]

        shared_layer = get_shared_layer(self)
        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)
        awswrangler = get_awswrangler_layer(self, replica_region)

        dr_actions_statement = cdk.aws_iam.PolicyStatement(
            actions=[
                "s3:*",
            ],
            resources=[
                bucket.bucket_arn,
                bucket.bucket_arn + "/*",
            ],
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

        self.queue = cdk.aws_sqs.Queue(
            self,
            id="ark-sqs-dr-recovery-process",
            queue_name=self.STACK_PREFIX + ENV["SQS_RECOVERY_PROCESS"],
            visibility_timeout=cdk.Duration.seconds(60),
        )

        self.lambda_function_2 = build_lambda_function(
            self,
            DISTRIBUTE_CODE_DIR,
            handler="distribute_export.handler",
            layers=[shared_layer, qldb_layer, qldb_reqs],
            description="dr qldb export lambda",
            env={
                "DR_BUCKET_NAME": bucket.bucket_name,
                "SQS_QUEUE_URL": self.queue.queue_url,
                "LOG_LEVEL": "INFO",
            },
            name="distribute-export",
            is_replication=True,
        )

        sqs_actions_statement = cdk.aws_iam.PolicyStatement(
            actions=[
                "sqs:SendMessage",
            ],
            resources=[self.queue.queue_arn],
        )

        dr_policy_2 = cdk.aws_iam.Policy(
            self,
            "ark-dr-export-policy2",
            policy_name="ark-dr-export-policy2",
            statements=[
                dr_actions_statement,
                dr_actions_statement2,
                sqs_actions_statement,
            ],
        )

        self.lambda_function_2.role.attach_inline_policy(dr_policy_2)

        self.restore_function = build_qldb_lambda_function(
            self,
            RESTORE_CODE_DIR,
            handler="restore_qldb.handler",
            layers=[shared_layer, qldb_layer, qldb_reqs, awswrangler],
            description="dr qldb restore lambda",
            env={
                "LOG_LEVEL": "INFO",
            },
            cdk_env=kwargs["env"],
            is_replication=True,
        )

        bucket.grant_read(self.restore_function.role)

        # Adding DR sqs queue as source for this function
        event_source = cdk.aws_lambda_event_sources.SqsEventSource(self.queue)
        self.restore_function.add_event_source(event_source)
        self.restore_function.role.attach_inline_policy(dr_policy)
