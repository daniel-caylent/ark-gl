#!/usr/bin/env python3
import os

import aws_cdk as cdk

from app.accounts.infrastructure import (
    AccountsGetStack,
)

app = cdk.App()


accounts = AccountsGetStack(app, "ark-gl-accounts-get-stack")

app.synth()
