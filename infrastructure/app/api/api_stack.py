from constructs import Construct

from ..base_stack import BaseStack

from ..get_cdk import build_api_gateway

from .api_account_attribute_nested_stack import AccountAttributesNestedStack
from .api_account_nested_stack import AccountNestedStack
from .api_ledger_nested_stack import LedgerNestedStack

from aws_cdk import aws_logs as logs, aws_apigateway as apigtw


class ApiStack(BaseStack):

    api_resources = {}

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api = build_api_gateway(self, "ark-gl-rest-api", deploy=False, cloud_watch_role=True)

        self.api.root.add_method("ANY")

        AccountAttributesNestedStack(self, "ark-gl-account-attributes-api-nested", self.api.rest_api_id, self.api.rest_api_root_resource_id)

        AccountNestedStack(self, "ark-gl-account-api-nested", self.api.rest_api_id, self.api.rest_api_root_resource_id)

        LedgerNestedStack(self, "ark-gl-ledger-api-nested", self.api.rest_api_id, self.api.rest_api_root_resource_id)

        deployment = apigtw.Deployment(self, "ark-gl-rest-api-deployment", api=self.api)

        log_group = logs.LogGroup(self, "api-logs")

        apigtw.Stage(self, "v1",
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
