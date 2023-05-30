from constructs import Construct

from ..base_nested_stack import BaseNestedStack

from ..get_cdk import (
    get_api_gateway_from_attributes,
    get_lambda_function_from_arn,
    build_lambda_integration,
    get_imported_value,
)


class JournalEntryNestedStack(BaseNestedStack):
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

        journal_entry_resource = rest_api.root.add_resource("journal-entries")
        journal_entry_id_resource = journal_entry_resource.add_resource(
            "{journalEntryId}"
        )

        self.__register_journal_entry_get_method(journal_entry_resource)
        self.__register_journal_entry_post_method(journal_entry_resource)
        self.__register_journal_entry_get_by_id_method(journal_entry_id_resource)
        self.__register_journal_entry_put_method(journal_entry_id_resource)

    def __register_journal_entry_get_by_id_method(self, resource):
        ark_journal_entry_get_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-get-by-id-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-journal-entries-get-by-id-function-arn",
            ark_journal_entry_get_function_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-get-by-id"
        )

        method = resource.add_method("GET", lambda_integration)

        self.methods.append(method)

    def __register_journal_entry_get_method(self, resource):
        ark_journal_entry_get_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-get-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-journal-entries-get-function-arn",
            ark_journal_entry_get_function_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-get"
        )

        method = resource.add_method("GET", lambda_integration)

        self.methods.append(method)

    def __register_journal_entry_post_method(self, resource):
        ark_journal_entry_post_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-post-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-journal-entries-post-function-arn",
            ark_journal_entry_post_function_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-post"
        )

        method = resource.add_method("POST", lambda_integration)

        self.methods.append(method)


    def __register_journal_entry_put_method(self, resource):
        ark_journal_entry_put_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-put-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-journal-entries-put-function-arn",
            ark_journal_entry_put_function_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-put"
        )

        method = resource.add_method("PUT", lambda_integration)

        self.methods.append(method)
