from constructs import Construct

from ..base_stack import BaseStack

from ..get_cdk import build_api_gateway

from .api_account_attribute_nested_stack import AccountAttributesNestedStack
from .api_account_nested_stack import AccountNestedStack
from .api_ledger_nested_stack import LedgerNestedStack
from .api_deploy_stack import DeployStack

from aws_cdk import aws_logs as logs, aws_apigateway as apigtw


class ApiStack(BaseStack):

    api_resources = {}

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api = build_api_gateway(self, "ark-gl-rest-api", deploy=False, cloud_watch_role=True)

        self.api.root.add_method("ANY")

        account_attributes_nested_stack=AccountAttributesNestedStack(
            self,
            "ark-gl-account-attributes-api-nested",
            self.api.rest_api_id,
            self.api.rest_api_root_resource_id
        )

        account_nested_stack=AccountNestedStack(
            self,
            "ark-gl-account-api-nested",
            self.api.rest_api_id,
            self.api.rest_api_root_resource_id
        )

        ledger_nested_stack=LedgerNestedStack(
            self,
            "ark-gl-ledger-api-nested",
            self.api.rest_api_id,
            self.api.rest_api_root_resource_id
        )

        methods = []
        methods.extend(account_attributes_nested_stack.methods)
        methods.extend(account_nested_stack.methods)
        methods.extend(ledger_nested_stack.methods)

        DeployStack(self, "ark-gl-rest-api-deploy", self.api.rest_api_id, methods)
