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

app = cdk.App()

AccountAttributesGetStack(app, "ark-gl-account-attributes-get-stack")
AccountsGetStack(app, "ark-gl-accounts-get-stack")
AccountsPostStack(app, "ark-gl-accounts-post-stack")

cdk.Tags.of(app).add('project', 'Ark PES')
app.synth()
