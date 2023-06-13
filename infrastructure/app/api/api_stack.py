from constructs import Construct
from datetime import datetime

from shared.base_stack import BaseStack

from shared.get_cdk import (
    build_api_gateway,
    build_api_gateway_deployment,
    build_api_gateway_stage,
)

from aws_cdk import aws_apigateway as apigtw, aws_logs as logs


class ApiStack(BaseStack):
    api_resources = {}

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api = build_api_gateway(
            self,
            self.STACK_PREFIX + "ark-gl-rest-api",
            deploy=False,
            cloud_watch_role=True,
        )

        self.api.root.add_method("ANY")
