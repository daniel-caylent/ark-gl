from constructs import Construct

from shared.base_nested_stack import BaseNestedStack

from shared.get_cdk import (
    get_api_gateway_from_attributes,
    get_lambda_function_from_arn,
    build_lambda_integration,
    get_imported_value
)

class LedgerNestedStack(BaseNestedStack):

    methods = []

    def __init__(self, scope: Construct, id: str, rest_api_id: str, root_resource_id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api = get_api_gateway_from_attributes(self, 'rest-api', rest_api_id=rest_api_id, root_resource_id=root_resource_id)

        ledger_resource = rest_api.root.add_resource('ledgers')
        ledger_id_resource = ledger_resource.add_resource('{ledgerId}')
        ledger_state_resource = ledger_id_resource.add_resource('state')

        self.__register_ledger_get_method(ledger_resource)
        self.__register_ledger_post_method(ledger_resource)
        self.__register_ledger_get_by_id_method(ledger_id_resource)
        self.__register_ledger_put_method(ledger_id_resource)
        self.__register_ledger_delete_method(ledger_id_resource)
        self.__register_ledger_state_method(ledger_state_resource)


    def __register_ledger_get_method(self, resource):
        ark_ledger_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-ledger-get-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-ledger-get-function-arn", ark_ledger_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "ledger-get")

        method = resource.add_method(
            "GET",
            lambda_integration)

        self.methods.append(method)


    def __register_ledger_get_by_id_method(self, resource):
        ark_ledger_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-ledger-get-by-id-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-ledger-get-by-id-function-arn", ark_ledger_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "ledger-get-by-id")

        method = resource.add_method(
            "GET",
            lambda_integration)

        self.methods.append(method)

    def __register_ledger_post_method(self, resource):
        ark_ledger_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-ledger-post-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-ledger-post-function-arn", ark_ledger_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "ledger-post")

        method = resource.add_method(
            "POST",
            lambda_integration)

        self.methods.append(method)

    def __register_ledger_put_method(self, resource):
        ark_ledger_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-ledger-put-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-ledger-put-function-arn", ark_ledger_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "ledger-put")

        method = resource.add_method(
            "PUT",
            lambda_integration)

        self.methods.append(method)

    def __register_ledger_delete_method(self, resource):
        ark_ledger_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-ledger-delete-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-ledger-delete-function-arn", ark_ledger_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "ledger-delete")

        method = resource.add_method(
            "DELETE",
            lambda_integration)

        self.methods.append(method)

    def __register_ledger_state_method(self, resource):
        ark_ledger_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-ledger-state-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-ledger-state-function-arn", ark_ledger_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "ledger-state")

        method = resource.add_method(
            "PUT",
            lambda_integration)

        self.methods.append(method)
