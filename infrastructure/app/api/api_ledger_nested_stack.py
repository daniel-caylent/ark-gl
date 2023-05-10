from constructs import Construct

from ..base_nested_stack import BaseNestedStack

from ..get_cdk import (
    get_api_gateway_from_attributes,
    get_lambda_function_from_arn,
    build_lambda_integration,
    get_imported_value
)

class LedgerNestedStack(BaseNestedStack):
    def __init__(self, scope: Construct, id: str, rest_api_id: str, root_resource_id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api = get_api_gateway_from_attributes(self, 'rest-api', rest_api_id=rest_api_id, root_resource_id=root_resource_id)

        ledger_resource = rest_api.root.add_resource('ledgers')
        ledger_id_resource = ledger_resource.add_resource('{ledgerId}')


        self.__register_ledger_get_method(ledger_resource)

        self.__register_ledger_get_by_id_method(ledger_id_resource)


    def __register_ledger_get_method(self, resource):
        ark_ledger_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-ledger-get-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-ledger-get-function-arn", ark_ledger_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "ledger-get")

        resource.add_method(
            "GET",
            lambda_integration)


    def __register_ledger_get_by_id_method(self, resource):
        ark_ledger_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-ledger-get-by-id-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-ledger-get-by-id-function-arn", ark_ledger_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "ledger-get-by-id")

        resource.add_method(
            "GET",
            lambda_integration)