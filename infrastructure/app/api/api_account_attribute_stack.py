from constructs import Construct

from shared.base_stack import BaseStack

from shared.get_cdk import (
    get_api_gateway_from_attributes,
    get_lambda_function_from_arn,
    build_lambda_integration,
    get_imported_value,
)


class AccountAttributesStack(BaseStack):
    methods = []

    def __init__(
        self,
        scope: Construct,
        id: str,
        rest_api_id: str,
        root_resource_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api = get_api_gateway_from_attributes(
            self, "rest-api", rest_api_id=rest_api_id, root_resource_id=root_resource_id
        )

        ark_account_get_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-account-attribute-get-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self, "ark-account-attribute-get-function-arn", ark_account_get_function_arn
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "account-attribute-get"
        )

        method = rest_api.root.add_resource("account-attributes").add_method(
            "GET", lambda_integration
        )

        self.methods.append(method)
