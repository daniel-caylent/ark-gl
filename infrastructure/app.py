#!/usr/bin/env python3
import os

import aws_cdk as cdk

from app.account_attributes import (
    AccountAttributesGetStack,
)

from app.accounts import (
    AccountsGetStack,
    AccountsPostStack,
    AccountsGetByIdStack,
    AccountsPutStack,
    AccountsStateStack,
    AccountsUploadStack,
    AccountsCopyStack,
    AccountsDeleteStack,
)

from app.ledgers import (
    LedgersGetStack,
    LedgersGetByIdStack,
    LedgersPostStack,
    LedgersPutStack,
    LedgersDeleteStack,
    LedgersStateStack,
)

from app.journal_entries import (
    JournalEntriesGetByIdStack,
    JournalEntriesGetStack,
    JournalEntriesPostStack,
    JournalEntriesPutStack,
    JournalEntriesDeleteStack,
    JournalEntriesStateStack,
)

from app.api.api_account_attribute_stack import (
    AccountAttributesStack
)

from app.api.api_accounts_stack import (
    AccountsStack
)

from app.api.api_ledgers_stack import (
    LedgersStack
)

from app.api.stage_stack import (
    StageStack
)

from env import ENV
from shared.vpc_stack import VpcStack
from shared.utils import get_stack_prefix
from app.api.api_stack import ApiStack

from constructs import DependencyGroup


cdk_env = cdk.Environment(
    account=os.getenv("AWS_ACCOUNT"), region=os.getenv("AWS_REGION")
)

app = cdk.App()

vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=cdk_env)

account_attributes_get_stack = AccountAttributesGetStack(
    app,
    "ark-gl-account-attributes-get-stack",
    env=cdk_env,
)
account_attributes_get_stack.add_dependency(vpc_stack)

accounts_get_stack = AccountsGetStack(app, "ark-gl-accounts-get-stack", env=cdk_env)
accounts_get_stack.add_dependency(vpc_stack)

accounts_get_by_id_stack = AccountsGetByIdStack(
    app, "ark-gl-accounts-get-by-id-stack", env=cdk_env
)
accounts_get_by_id_stack.add_dependency(vpc_stack)
#
accounts_post_stack = AccountsPostStack(app, "ark-gl-accounts-post-stack", env=cdk_env)
accounts_post_stack.add_dependency(vpc_stack)

accounts_delete_stack = AccountsDeleteStack(
    app, "ark-gl-accounts-delete-stack", env=cdk_env
)
accounts_delete_stack.add_dependency(vpc_stack)

accounts_put_stack = AccountsPutStack(app, "ark-gl-accounts-put-stack", env=cdk_env)
accounts_put_stack.add_dependency(vpc_stack)

accounts_state_stack = AccountsStateStack(
    app, "ark-gl-accounts-state-stack", env=cdk_env
)
accounts_state_stack.add_dependency(vpc_stack)

accounts_upload_stack = AccountsUploadStack(
    app, "ark-gl-accounts-upload-stack", env=cdk_env
)
accounts_upload_stack.add_dependency(vpc_stack)

ledgers_get_stack = LedgersGetStack(app, "ark-gl-ledgers-get-stack", env=cdk_env)
ledgers_get_stack.add_dependency(vpc_stack)

ledgers_get_by_id_stack = LedgersGetByIdStack(
    app, "ark-gl-ledgers-get-by-id-stack", env=cdk_env
)
ledgers_get_by_id_stack.add_dependency(vpc_stack)

ledgers_post_stack = LedgersPostStack(app, "ark-gl-ledgers-post-stack", env=cdk_env)
ledgers_post_stack.add_dependency(vpc_stack)

ledgers_put_stack = LedgersPutStack(app, "ark-gl-ledgers-put-stack", env=cdk_env)
ledgers_put_stack.add_dependency(vpc_stack)

ledgers_delete_stack = LedgersDeleteStack(
    app, "ark-gl-ledgers-delete-stack", env=cdk_env
)
ledgers_delete_stack.add_dependency(vpc_stack)

ledgers_state_stack = LedgersStateStack(app, "ark-gl-ledgers-state-stack", env=cdk_env)
ledgers_state_stack.add_dependency(vpc_stack)
#
#journal_entries_get_by_id_stack = JournalEntriesGetByIdStack(
#    app, "ark-gl-journal-entries-get-by-id-stack", env=cdk_env
#)
#journal_entries_get_by_id_stack.add_dependency(vpc_stack)
#
#journal_entries_get_stack = JournalEntriesGetStack(
#    app, "ark-gl-journal-entries-get-stack", env=cdk_env
#)
#journal_entries_get_stack.add_dependency(vpc_stack)
#
#journal_entries_post_stack = JournalEntriesPostStack(
#    app, "ark-gl-journal-entries-post-stack", env=cdk_env
#)
#journal_entries_post_stack.add_dependency(vpc_stack)
#
#journal_entries_put_stack = JournalEntriesPutStack(
#    app, "ark-gl-journal-entries-put-stack", env=cdk_env
#)
#journal_entries_put_stack.add_dependency(vpc_stack)
#
#journal_entries_delete_stack = JournalEntriesDeleteStack(
#    app, "ark-gl-journal-entries-delete-stack", env=cdk_env
#)
#journal_entries_delete_stack.add_dependency(vpc_stack)
#
#journal_entries_state_stack = JournalEntriesStateStack(
#    app, "ark-gl-journal-entries-state-stack", env=cdk_env
#)
#journal_entries_state_stack.add_dependency(vpc_stack)
#
dependency_group = DependencyGroup()
dependency_group.add(vpc_stack)

#dependency_group.add(journal_entries_get_by_id_stack)
#dependency_group.add(journal_entries_get_stack)
#dependency_group.add(journal_entries_post_stack)
#dependency_group.add(journal_entries_put_stack)
#dependency_group.add(journal_entries_state_stack)
#dependency_group.add(journal_entries_delete_stack)

rest_api = ApiStack(app, "ark-gl-api-stack", env=cdk_env)

rest_api.node.add_dependency(
    dependency_group
)

account_attributes_dependency_group = DependencyGroup()
account_attributes_dependency_group.add(rest_api)
account_attributes_dependency_group.add(account_attributes_get_stack)

api_account_attributes_stack = AccountAttributesStack(
    app,
    "ark-gl-api-account-attributes",
    rest_api.api.rest_api_id,
    rest_api.api.rest_api_root_resource_id,
    env=cdk_env
)

api_account_attributes_stack.node.add_dependency(
    account_attributes_dependency_group
)

accounts_dependency_group = DependencyGroup()
accounts_dependency_group.add(rest_api)
accounts_dependency_group.add(account_attributes_get_stack)
accounts_dependency_group.add(account_attributes_get_stack)
accounts_dependency_group.add(accounts_get_stack)
accounts_dependency_group.add(accounts_get_by_id_stack)
accounts_dependency_group.add(accounts_post_stack)
accounts_dependency_group.add(accounts_delete_stack)
accounts_dependency_group.add(accounts_put_stack)
accounts_dependency_group.add(accounts_state_stack)
accounts_dependency_group.add(accounts_upload_stack)

api_accounts_stack = AccountsStack(
    app,
    "ark-gl-api-accounts",
    rest_api.api.rest_api_id,
    rest_api.api.rest_api_root_resource_id,
    env=cdk_env
)

api_accounts_stack.node.add_dependency(
    accounts_dependency_group
)

ledgers_dependency_group = DependencyGroup()
ledgers_dependency_group.add(rest_api)
ledgers_dependency_group.add(ledgers_get_stack)
ledgers_dependency_group.add(ledgers_get_by_id_stack)
ledgers_dependency_group.add(ledgers_post_stack)
ledgers_dependency_group.add(ledgers_put_stack)
ledgers_dependency_group.add(ledgers_delete_stack)
ledgers_dependency_group.add(ledgers_state_stack)

api_ledgers_stack = LedgersStack(
    app,
    "ark-gl-api-ledgers",
    rest_api.api.rest_api_id,
    rest_api.api.rest_api_root_resource_id,
    env=cdk_env
)

api_ledgers_stack.node.add_dependency(
    ledgers_dependency_group
)


methods = []

stage_dependency_group = DependencyGroup()

if os.getenv("STACKS"):

    print(f"Stacks loaded: {os.getenv('STACKS')}")

    stacks = os.getenv("STACKS").split(",")

    if get_stack_prefix() + "ark-gl-api-account-attributes" in stacks:
        methods.extend(api_account_attributes_stack.methods)
        stage_dependency_group.add(api_account_attributes_stack)

    if get_stack_prefix() + "ark-gl-api-accounts" in stacks:
        methods.extend(api_accounts_stack.methods)
        stage_dependency_group.add(api_accounts_stack)

    if get_stack_prefix() + "ark-gl-api-ledgers" in stacks:
        methods.extend(api_ledgers_stack.methods)
        stage_dependency_group.add(api_ledgers_stack)

api_stage_stack = StageStack(app, "ark-gl-api-stage-stack", rest_api.api, methods, env=cdk_env)

api_stage_stack.node.add_dependency(stage_dependency_group)

cdk.Tags.of(app).add("project", "Ark PES")
cdk.Tags.of(app).add(ENV["MAP_TAG"], ENV["MAP_VALUE"])

app.synth()
