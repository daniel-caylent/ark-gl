import aws_cdk as cdk

import os

from shared.vpc_stack import VpcStack
from app.reconciliation import (
    SQSStack,
    AccountsReconciliationStack,
    LedgersReconciliationStack,
    LoadBalancerJournalEntriesStack,
    JournalEntriesReconciliationStack,
    StepFunctionStack,
)
from env import ENV


cdk_env = cdk.Environment(  # Caylent env:
    account=os.getenv("AWS_ACCOUNT"),  # '131578276461'
    region=os.getenv("AWS_REGION"),  # 'us-east-2'
)

app = cdk.App()


sqs_stack = SQSStack(app, "ark-sqs-stack", env=cdk_env)

vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=cdk_env)

accounts_reconciliation_stack = AccountsReconciliationStack(
    app, "ark-accounts-reconciliation-stack", env=cdk_env
)
accounts_reconciliation_stack.add_dependency(vpc_stack)

load_balancer_reconciliation_stack = LoadBalancerJournalEntriesStack(
    app, "ark-load-balancer-reconciliation-stack", env=cdk_env
)
load_balancer_reconciliation_stack.add_dependency(vpc_stack)

journals_reconciliation_stack = JournalEntriesReconciliationStack(
    app, "ark-journals-reconciliation-stack", queue=sqs_stack.queue, env=cdk_env
)
journals_reconciliation_stack.add_dependency(vpc_stack)

ledgers_reconciliation_stack = LedgersReconciliationStack(
    app, "ark-ledgers-reconciliation-stack", env=cdk_env
)
ledgers_reconciliation_stack.add_dependency(vpc_stack)

step_function_stack = StepFunctionStack(
    app,
    "ark-stepfunction-reconciliation-stack",
    accounts_reconciliation_lambda=accounts_reconciliation_stack.lambda_function,
    ledgers_reconciliation_lambda=ledgers_reconciliation_stack.lambda_function,
    journals_loadbalancer_lambda=load_balancer_reconciliation_stack.lambda_function,
    env=cdk_env,
)
step_function_stack.add_dependency(vpc_stack)

cdk.Tags.of(app).add("project", "Ark PES")
cdk.Tags.of(app).add(ENV["MAP_TAG"], ENV["MAP_VALUE"])

app.synth()
