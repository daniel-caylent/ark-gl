from constructs import Construct

from ..base_nested_stack import BaseNestedStack

from ..get_cdk import (
    get_api_gateway_from_attributes,
    get_lambda_function_from_arn,
    build_lambda_integration,
    get_imported_value
)

class AccountNestedStack(BaseNestedStack):
    def __init__(self, scope: Construct, id: str, rest_api_id: str, root_resource_id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api = get_api_gateway_from_attributes(self, 'rest-api', rest_api_id=rest_api_id, root_resource_id=root_resource_id)

        account_resource = rest_api.root.add_resource('accounts')
        account_id_resource = account_resource.add_resource('{accountId}')

        self.__register_account_get_method(account_resource)
        self.__register_account_post_method(account_resource)

        self.__register_account_put_method(account_id_resource)
        self.__register_account_get_by_id_method(account_id_resource)
        self.__register_account_delete_method(account_id_resource)
        self.__register_account_state_method(account_id_resource)
        self.__register_account_upload_method(account_id_resource)


    def __register_account_get_method(self, resource):
        ark_account_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-account-get-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-account-get-function-arn", ark_account_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "accounts-get")

        resource.add_method(
            "GET",
            lambda_integration)


    def __register_account_get_by_id_method(self, resource):
        ark_account_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-account-get-by-id-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-account-get-by-id-function-arn", ark_account_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "accounts-get-by-id")

        resource.add_method(
            "GET",
            lambda_integration)


    def __register_account_post_method(self, resource):
        ark_account_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-account-post-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-account-post-function-arn", ark_account_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "accounts-post")

        resource = resource.add_method(
            "POST",
            lambda_integration)


    def __register_account_delete_method(self, resource):
        ark_account_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-account-delete-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-account-delete-function-arn", ark_account_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "accounts-delete")

        resource.add_method(
            "DELETE",
            lambda_integration)


    def __register_account_put_method(self, resource):
        ark_account_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-account-put-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-account-put-function-arn", ark_account_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "accounts-put")

        resource.add_method(
            "PUT",
            lambda_integration)


    def __register_account_state_method(self, resource):
        ark_account_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-account-state-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-account-state-function-arn", ark_account_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "accounts-state")

        resource.add_resource("state").add_method(
            "PUT",
            lambda_integration)


    def __register_account_upload_method(self, resource):
        ark_account_get_function_arn = get_imported_value(self.STACK_PREFIX + "ark-account-upload-function-arn")

        lambda_function = get_lambda_function_from_arn(self, "ark-account-upload-function-arn", ark_account_get_function_arn)

        lambda_integration = build_lambda_integration(
            self,
            lambda_function,
            self.STACK_PREFIX + "accounts-upload")

        resource.add_method(
            "POST",
            lambda_integration)