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
    AccountsCommitStack
)

from app.vpc_stack import VpcStack
from app.env import ENV

from pipeline import PipelineStack


cdk_env=cdk.Environment(                     # Caylent env:
    account = os.getenv('AWS_ACCOUNT'),  # '131578276461'
    region = os.getenv('AWS_REGION')     # 'us-east-2'
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

PipelineStack(app, "ark-gl-pipeline-stack")

cdk.Tags.of(app).add('project', 'Ark PES')
cdk.Tags.of(app).add(ENV['MAP_TAG'], ENV['MAP_VALUE'])

app.synth()