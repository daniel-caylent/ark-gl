from constructs import Construct

from shared.base_stack import BaseStack

from shared.get_cdk import (
    get_api_gateway_from_attributes,
    get_lambda_function_from_arn,
    build_lambda_integration,
    get_imported_value,
)


class JournalEntriesStack(BaseStack):
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
        journal_search_resource = journal_entry_resource.add_resource("search")
        journal_upload_resource = journal_entry_resource.add_resource("upload")
        journal_delete_resource = journal_entry_resource.add_resource("delete")
        journal_export_resource = journal_entry_resource.add_resource("export")
        journal_bulk_state_resource = journal_entry_resource.add_resource("state")
        journal_entry_id_resource = journal_entry_resource.add_resource(
            "{journalEntryId}"
        )
        journal_entry_state_resource = journal_entry_id_resource.add_resource("state")

        self.__register_journal_entry_get_method(journal_search_resource)
        self.__register_journal_entry_post_method(journal_entry_resource)
        self.__register_journal_entry_put_method(journal_entry_id_resource)
        self.__register_journal_entry_get_by_id_method(journal_entry_id_resource)
        self.__register_journal_entry_delete_method(journal_entry_id_resource)
        self.__register_journal_entry_state_method(journal_entry_state_resource)
        self.__register_journal_entry_upload_method(journal_upload_resource)
        self.__register_journal_entry_bulk_delete_method(journal_delete_resource)
        self.__register_journal_entry_export_method(journal_export_resource)
        self.__register_journal_entry_bulk_state_method(journal_bulk_state_resource)


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

        method = resource.add_method("POST", lambda_integration)

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

    def __register_journal_entry_state_method(self, resource):
        ark_journal_entry_state_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-state-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-journal-entries-state-function-arn",
            ark_journal_entry_state_function_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-state"
        )

        method = resource.add_method("PUT", lambda_integration)

        self.methods.append(method)

    def __register_journal_entry_delete_method(self, resource):
        ark_journal_entry_delete_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-delete-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-journal-entries-delete-function-arn",
            ark_journal_entry_delete_function_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-delete"
        )

        method = resource.add_method("DELETE", lambda_integration)

        self.methods.append(method)

    def __register_journal_entry_bulk_delete_method(self, resource):
        ark_journal_entry_delete_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-bulk-delete-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-journal-entries-bulk-delete-function-arn",
            ark_journal_entry_delete_function_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-bulk-delete"
        )

        method = resource.add_method("POST", lambda_integration)

        self.methods.append(method)


    def __register_journal_entry_export_method(self, resource):
        ark_journal_entry_delete_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-export-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-journal-entries-export-function-arn",
            ark_journal_entry_delete_function_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-export"
        )

        method = resource.add_method("POST", lambda_integration)

        self.methods.append(method)


    def __register_journal_entry_upload_method(self, resource):
        ark_journal_entry_upload_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-upload-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self,
            "ark-journal-entries-upload-function-arn",
            ark_journal_entry_upload_function_arn,
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-upload"
        )

        method = resource.add_method("POST", lambda_integration)

        self.methods.append(method)


    def __register_journal_entry_bulk_state_method(self, resource):
        ark_journal_entries_bulk_state_function_arn = get_imported_value(
            self.STACK_PREFIX + "ark-journal-entries-bulk-state-function-arn"
        )

        lambda_function = get_lambda_function_from_arn(
            self, "ark-journal-entries-bulk-state-function-arn", ark_journal_entries_bulk_state_function_arn
        )

        lambda_integration = build_lambda_integration(
            self, lambda_function, self.STACK_PREFIX + "journal-entries-bulk-state"
        )

        method = resource.add_method("PUT", lambda_integration)

        self.methods.append(method)
