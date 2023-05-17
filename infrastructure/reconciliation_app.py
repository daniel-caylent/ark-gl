import aws_cdk as cdk

import os

import sys
 
# setting path
#sys.path.append('../')
from app.vpc_stack import VpcStack
from app.reconciliation import (SQSStack, SNSStack)
from app.reconciliation import AccountsReconciliationStack
from app.reconciliation import LedgersReconciliationStack
from app.reconciliation import LoadBalancerJournalEntriesStack
from env import ENV


cdk_env=cdk.Environment(                     # Caylent env:
    account = os.getenv('AWS_ACCOUNT'),  # '131578276461'
    region = os.getenv('AWS_REGION')     # 'us-east-2'
)

app = cdk.App()


sqs_stack = SQSStack(
    app, "ark-sqs-stack", env=cdk_env
)

sns_stack = SNSStack(
    app, "ark-sns-stack", env=cdk_env
)

vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=cdk_env)

accounts_reconciliation_stack = AccountsReconciliationStack(app, "ark-accounts-reconciliation-stack", env=cdk_env)
accounts_reconciliation_stack.add_dependency(vpc_stack)

load_balancer_reconciliation_stack = LoadBalancerJournalEntriesStack(app, "ark-load-balancer-reconciliation-stack", env=cdk_env)
load_balancer_reconciliation_stack.add_dependency(vpc_stack)

ledgers_reconciliation_stack = LedgersReconciliationStack(app, "ark-ledgers-reconciliation-stack", env=cdk_env)
ledgers_reconciliation_stack.add_dependency(vpc_stack)

cdk.Tags.of(app).add('project', 'Ark PES')
cdk.Tags.of(app).add(ENV['MAP_TAG'], ENV['MAP_VALUE'])

app.synth()