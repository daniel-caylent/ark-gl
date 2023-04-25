#!/usr/bin/env python3
import os

import aws_cdk as cdk

from app.account_attributes import (
    AccountAttributesGetStack,
)

from app.accounts import (
    AccountsGetStack,
    AccountsPostStack
)

from app.vpc_stack import VpcStack

from pipeline import PipelineStack


env=cdk.Environment(                             # Caylent env:
    account = '131578276461', # '131578276461'
    region = 'us-east-2'    #
)

app = cdk.App()

vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=env)

AccountAttributesGetStack(
    app, "ark-gl-account-attributes-get-stack", env=env
)

AccountsGetStack(
    app, "ark-gl-accounts-get-stack", env=env
)

AccountsPostStack(
    app, "ark-gl-accounts-post-stack", env=env
)


PipelineStack(app, "ark-gl-pipeline-stack")


cdk.Tags.of(app).add('project', 'Ark PES')
app.synth()
