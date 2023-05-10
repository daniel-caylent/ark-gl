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
    AccountsDeleteStack
)

from app.ledgers import (
    LedgersGetStack,
    LedgersGetByIdStack
)

from app.env import ENV
from app.vpc_stack import VpcStack
from app.api.api_stack import ApiStack

from constructs import DependencyGroup


cdk_env=cdk.Environment(
    account = os.getenv('AWS_ACCOUNT'),
    region = os.getenv('AWS_REGION')
)

app = cdk.App()

vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=cdk_env)

account_attributes_get_stack=AccountAttributesGetStack(
    app, "ark-gl-account-attributes-get-stack",
    env=cdk_env,
)
account_attributes_get_stack.add_dependency(vpc_stack)

accounts_get_stack=AccountsGetStack(
    app, "ark-gl-accounts-get-stack",
    env=cdk_env
)
accounts_get_stack.add_dependency(vpc_stack)

accounts_get_by_id_stack=AccountsGetByIdStack(
    app, "ark-gl-accounts-get-by-id-stack", env=cdk_env
)
accounts_get_by_id_stack.add_dependency(vpc_stack)

accounts_post_stack=AccountsPostStack(
    app, "ark-gl-accounts-post-stack", env=cdk_env
)
accounts_post_stack.add_dependency(vpc_stack)

accounts_delete_stack=AccountsDeleteStack(
    app, "ark-gl-accounts-delete-stack", env=cdk_env
)
accounts_delete_stack.add_dependency(vpc_stack)

accounts_put_stack=AccountsPutStack(
    app, "ark-gl-accounts-put-stack", env=cdk_env
)
accounts_put_stack.add_dependency(vpc_stack)

accounts_state_stack=AccountsStateStack(
    app, "ark-gl-accounts-state-stack", env=cdk_env
)
accounts_state_stack.add_dependency(vpc_stack)

accounts_upload_stack=AccountsUploadStack(
    app, "ark-gl-accounts-upload-stack", env=cdk_env
)
accounts_upload_stack.add_dependency(vpc_stack)

ledgers_get_stack=LedgersGetStack(
    app, "ark-gl-ledgers-get-stack", env=cdk_env
)

ledgers_get_stack.add_dependency(vpc_stack)

ledgers_get_by_id_stack=LedgersGetByIdStack(
    app, "ark-gl-ledgers-get-by-id-stack", env=cdk_env
)
ledgers_get_by_id_stack.add_dependency(vpc_stack)

dependency_group = DependencyGroup()
dependency_group.add(vpc_stack)
dependency_group.add(account_attributes_get_stack)
dependency_group.add(accounts_get_stack)
dependency_group.add(accounts_get_by_id_stack)
dependency_group.add(accounts_post_stack)
dependency_group.add(accounts_delete_stack)
dependency_group.add(accounts_put_stack)
dependency_group.add(accounts_state_stack)
dependency_group.add(accounts_upload_stack)
dependency_group.add(ledgers_get_stack)
dependency_group.add(ledgers_get_by_id_stack)

rest_api = ApiStack(app, "ark-gl-api-stack", env=cdk_env).node.add_dependency(dependency_group)

# TODO: check if this method is still needed
AccountsCopyStack(
    app, "ark-gl-accounts-copy-stack", env=cdk_env
).add_dependency(vpc_stack)

cdk.Tags.of(app).add('project', 'Ark PES')
cdk.Tags.of(app).add(ENV['MAP_TAG'], ENV['MAP_VALUE'])

app.synth()
