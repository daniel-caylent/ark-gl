import aws_cdk as cdk

import os

import sys
 
# setting path
#sys.path.append('../')
from app.vpc_stack import VpcStack
from app.reconciliation import SQSStack
from app.reconciliation import AccountsReconciliationStack
from env import ENV


cdk_env=cdk.Environment(                     # Caylent env:
    account = os.getenv('AWS_ACCOUNT'),  # '131578276461'
    region = os.getenv('AWS_REGION')     # 'us-east-2'
)

app = cdk.App()


qldb_stack = SQSStack(
    app, "ark-sqs-stack", env=cdk_env
)
vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=cdk_env)

accounts_reconciliation_stack = AccountsReconciliationStack(app, "ark-accounts-reconciliation-stack", env=cdk_env)
accounts_reconciliation_stack.add_dependency(vpc_stack)

cdk.Tags.of(app).add('project', 'Ark PES')
cdk.Tags.of(app).add(ENV['MAP_TAG'], ENV['MAP_VALUE'])

app.synth()