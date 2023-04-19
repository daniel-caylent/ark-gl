#!/usr/bin/env python3
import os

import aws_cdk as cdk

from app.accounts.infrastructure import (
    AccountsGetStack,
)

from app.account_attributes.infrastructure import (
    AccountAttributesGetStack
)

app = cdk.App()

account_attributes = AccountAttributesGetStack(app, "ark-gl-account-attributes-get-stack")
accounts = AccountsGetStack(app, "ark-gl-accounts-get-stack")

app.synth()
