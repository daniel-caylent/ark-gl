from constructs import Construct

from shared.base_stack import BaseStack

from shared.get_cdk import (
    get_api_gateway_from_attributes,
    get_lambda_function_from_arn,
    build_lambda_integration,
    get_imported_value,
)


class ApiReportsStack(BaseStack):
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

        reports_resource = rest_api.root.add_resource("reports")

        reports_trial_balance_resource = reports_resource.add_resource("trial-balance")
        reports_trial_balance_detail_resource = reports_resource.add_resource("trial-balance-detail")
        self.__register_reports_trial_balance_method(reports_trial_balance_resource)
        self.__register_reports_trial_balance_detail_method(reports_trial_balance_detail_resource)

    def __register_reports_trial_balance_method(self, resource):
        trial_balance_arn = get_imported_value(
            self.STACK_PREFIX + "ark-reports-trial-balance-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-reports-trial-balance-function-arn",
            trial_balance_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "reports-trial-balance"
        )

        method = resource.add_method("GET", lambda_integration)

        self.methods.append(method)


    def __register_reports_trial_balance_detail_method(self, resource):
        trial_balance_arn = get_imported_value(
            self.STACK_PREFIX + "ark-reports-trial-balance-detail-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-reports-trial-balance-detail-function-arn",
            trial_balance_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "reports-trial-balance-detail"
        )

        method = resource.add_method("POST", lambda_integration)

        self.methods.append(method)
