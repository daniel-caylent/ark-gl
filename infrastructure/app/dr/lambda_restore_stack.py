import aws_cdk as cdk
from constructs import Construct
from pathlib import PurePath

from shared.get_cdk import build_qldb_lambda_function
from shared.layers import (
    get_shared_layer,
    get_qldb_layer,
    get_pyqldb_layer,
    get_awswrangler_layer,
)

from shared.base_stack import BaseStack
from shared.utils import DR_DIR

RESTORE_CODE_DIR = str(PurePath(DR_DIR, "restore"))


class LambdaRestoreStack(BaseStack):
    def __init__(self, scope: Construct, id: str,
                 bucket: cdk.aws_s3.Bucket,
                 queue: cdk.aws_sqs.Queue,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)
        awswrangler = get_awswrangler_layer(self)

        self.restore_function = build_qldb_lambda_function(
            self,
            RESTORE_CODE_DIR,
            handler="restore_qldb.handler",
            layers=[shared_layer, qldb_layer, qldb_reqs, awswrangler],
            description="dr qldb restore lambda",
            env={
                "LOG_LEVEL": "INFO",
            },
        )

        bucket.grant_read(self.restore_function.role)

        # Adding DR sqs queue as source for this function
        event_source = cdk.aws_lambda_event_sources.SqsEventSource(queue)
        self.restore_function.add_event_source(event_source)
