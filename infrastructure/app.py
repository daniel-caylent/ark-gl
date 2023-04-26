#!/usr/bin/env python3
import os

import aws_cdk as cdk

from app.account_attributes import (
    AccountAttributesGetStack,
)

from app.accounts import (
    AccountsGetStack,
    AccountsPostStack,
    AccountsGetByIdStack
)

from app.vpc_stack import VpcStack

from pipeline import PipelineStack


env=cdk.Environment(                     # Caylent env:
    account = os.getenv('AWS_ACCOUNT'),  # '131578276461'
    region = os.getenv('AWS_REGION')     # 'us-east-2'
)

app = cdk.App()

vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=env)

AccountAttributesGetStack(
    app, "ark-gl-account-attributes-get-stack", env=env
).add_dependency(vpc_stack)

AccountsGetStack(
    app, "ark-gl-accounts-get-stack", env=env
).add_dependency(vpc_stack)

AccountsPostStack(
    app, "ark-gl-accounts-post-stack", env=env
).add_dependency(vpc_stack)

AccountsGetByIdStack(
    app, "ark-gl-accounts-get-by-id-stack", env=env
).add_dependency(vpc_stack)

PipelineStack(app, "ark-gl-pipeline-stack")


cdk.Tags.of(app).add('project', 'Ark PES')
app.synth()
