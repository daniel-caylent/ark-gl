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

from pipeline import PipelineStack


env=cdk.Environment(                             # Caylent env:
    account = os.environ["CDK_DEFAULT_ACCOUNT"], # '131578276461'
    region = os.environ["CDK_DEFAULT_REGION"]    # 'us-east-2'
)

app = cdk.App()

AccountAttributesGetStack(app, "ark-gl-account-attributes-get-stack", env=env)
AccountsGetStack(app, "ark-gl-accounts-get-stack", env=env)
AccountsPostStack(app, "ark-gl-accounts-post-stack", env=env)

PipelineStack(app, "ark-gl-pipeline-stack")


cdk.Tags.of(app).add('project', 'Ark PES')
app.synth()
