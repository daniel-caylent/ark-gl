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
    AccountsCommitStack,
    AccountsUploadStack,
    AccountsCopyStack,
    AccountsDeleteStack
)

from app.ledgers import (
    LedgersGetStack,
    LedgersGetByIdStack
)

from app.vpc_stack import VpcStack

from app.env import ENV


cdk_env=cdk.Environment(
    account = os.getenv('AWS_ACCOUNT'),
    region = os.getenv('AWS_REGION')
)

app = cdk.App()

vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=cdk_env)

AccountAttributesGetStack(
    app, "ark-gl-account-attributes-get-stack", env=cdk_env
).add_dependency(vpc_stack)

AccountsGetStack(
    app, "ark-gl-accounts-get-stack", env=cdk_env
).add_dependency(vpc_stack)

AccountsPostStack(
    app, "ark-gl-accounts-post-stack", env=cdk_env
).add_dependency(vpc_stack)

AccountsGetByIdStack(
    app, "ark-gl-accounts-get-by-id-stack", env=cdk_env
).add_dependency(vpc_stack)

AccountsPutStack(
    app, "ark-gl-accounts-put-stack", env=cdk_env
).add_dependency(vpc_stack)

AccountsCommitStack(
    app, "ark-gl-accounts-commit-stack", env=cdk_env
).add_dependency(vpc_stack)

AccountsDeleteStack(
    app, "ark-gl-accounts-delete-stack", env=cdk_env
).add_dependency(vpc_stack)

AccountsUploadStack(
    app, "ark-gl-accounts-upload-stack", env=cdk_env
).add_dependency(vpc_stack)

AccountsCopyStack(
    app, "ark-gl-accounts-copy-stack", env=cdk_env
).add_dependency(vpc_stack)

LedgersGetStack(
    app, "ark-gl-ledgers-get-stack", env=cdk_env
).add_dependency(vpc_stack)

LedgersGetByIdStack(
    app, "ark-gl-ledgers-get-by-id-stack", env=cdk_env
).add_dependency(vpc_stack)

cdk.Tags.of(app).add('project', 'Ark PES')
cdk.Tags.of(app).add(ENV['MAP_TAG'], ENV['MAP_VALUE'])

app.synth()
