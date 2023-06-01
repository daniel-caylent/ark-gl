import aws_cdk as cdk
from constructs import Construct

from ...env import ENV
from ..base_stack import BaseStack


class SQSStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.queue = cdk.aws_sqs.Queue(
            self,
            id="ark-sqs-reconciliation",
            queue_name=self.STACK_PREFIX + ENV["sqs_name"],
            visibility_timeout=cdk.Duration.seconds(60),
        )

        cdk.CfnOutput(
            self,
            "sqs-reconciliation",
            value=self.queue.queue_name,
            export_name=self.STACK_PREFIX + ENV["sqs_name"],
        )
