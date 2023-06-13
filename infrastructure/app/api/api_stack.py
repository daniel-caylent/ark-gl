from constructs import Construct
from datetime import datetime

from shared.base_stack import BaseStack

from shared.get_cdk import (
    build_api_gateway,
    build_api_gateway_deployment,
    build_api_gateway_stage,
)

#from .api_account_attribute_nested_stack import AccountAttributesNestedStack
#from .api_account_nested_stack import AccountNestedStack
#from .api_ledger_nested_stack import LedgerNestedStack
from .api_journal_entry_nested_stack import JournalEntryNestedStack

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

        #account_attributes_nested_stack = AccountAttributesNestedStack(
        #    self,
        #    "ark-gl-account-attributes-api-nested",
        ##    self.api.rest_api_id,
        #    self.api.rest_api_root_resource_id,
        #)
#
        #account_nested_stack = AccountNestedStack(
        #    self,
        #    "ark-gl-account-api-nested",
        #    self.api.rest_api_id,
        #    self.api.rest_api_root_resource_id,
        #)
#
        #ledger_nested_stack = LedgerNestedStack(
        #    self,
        #    "ark-gl-ledger-api-nested",
        #    self.api.rest_api_id,
        #    self.api.rest_api_root_resource_id,
        #)
#
        #journal_entries_nested_stack = JournalEntryNestedStack(
        #    self,
        #    "ark-gl-journal-entries-api-nested",
        #    self.api.rest_api_id,
        #    self.api.rest_api_root_resource_id,
        #)
#
        #methods = []
        #methods.extend(account_attributes_nested_stack.methods)
        #methods.extend(account_nested_stack.methods)
        #methods.extend(ledger_nested_stack.methods)
        #methods.extend(journal_entries_nested_stack.methods)
#
        #deployment = build_api_gateway_deployment(
        #    self, "ark-gl-api-deployment-" + datetime.now().isoformat(), api=self.api
        #)
#
        #if methods:
        #    for method in methods:
        #        deployment.node.add_dependency(method)
#
        #deployment.add_to_logical_id(datetime.now().isoformat())
#
        #log_group = logs.LogGroup(self, "api-logs")
#
        #stage = build_api_gateway_stage(
        #    self,
        #    "ark-gl-api-stage-v1",
        #    stage_name="v1",
        #    deployment=deployment,
        #    metrics_enabled=True,
        #    access_log_destination=apigtw.LogGroupLogDestination(log_group),
        #    access_log_format=apigtw.AccessLogFormat.json_with_standard_fields(
        #        caller=False,
        #        http_method=True,
        #        ip=True,
        #        protocol=True,
        #        request_time=True,
        #        resource_path=True,
        #        response_length=True,
        #        status=True,
        #        user=True,
        #    ),
        #)
#
        #self.api.deployment_stage = stage
#