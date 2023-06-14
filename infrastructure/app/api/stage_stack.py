from constructs import Construct
from datetime import datetime

from shared.base_stack import BaseStack

from shared.get_cdk import (
    build_api_gateway,
    build_api_gateway_deployment,
    build_api_gateway_stage,
)

from aws_cdk import aws_apigateway as apigtw, aws_logs as logs


class StageStack(BaseStack):
    api_resources = {}

    def __init__(self, scope: Construct, id: str, api: Construct, methods: list, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        deployment = build_api_gateway_deployment(
            self, "ark-gl-api-deployment-" + datetime.now().isoformat(), api=api
        )

        if methods:
            for method in methods:
                deployment.node.add_dependency(method)

        deployment.add_to_logical_id(datetime.now().isoformat())

        log_group = logs.LogGroup(self, "api-logs")

        stage = build_api_gateway_stage(
            self,
            "ark-gl-api-stage-v1",
            stage_name="v1",
            deployment=deployment,
            metrics_enabled=True,
            access_log_destination=apigtw.LogGroupLogDestination(log_group),
            access_log_format=apigtw.AccessLogFormat.json_with_standard_fields(
                caller=False,
                http_method=True,
                ip=True,
                protocol=True,
                request_time=True,
                resource_path=True,
                response_length=True,
                status=True,
                user=True,
            ),
        )

        api.deployment_stage = stage
