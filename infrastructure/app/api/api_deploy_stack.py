from constructs import Construct

from ..base_nested_stack import BaseNestedStack

from typing import List

from ..get_cdk import (
    get_api_gateway_from_attributes,
    get_lambda_function_from_arn,
    build_lambda_integration,
    get_imported_value
)

from aws_cdk import aws_apigateway as apigtw, aws_logs as logs

class DeployStack(BaseNestedStack):
    def __init__(self, scope: Construct, id: str, rest_api_id: str, methods: List, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        deployment = apigtw.Deployment(self, "ark-gl-rest-api-deployment", api=apigtw.RestApi.from_rest_api_id(self, "RestApi", rest_api_id))

        if methods:
            for method in methods:
                deployment.node.add_dependency(method)

        log_group = logs.LogGroup(self, "api-logs")

        apigtw.Stage(self, "v1",
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
            )
        )
