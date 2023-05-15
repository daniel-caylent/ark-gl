import aws_cdk as cdk

import os

import sys
 
# setting path
sys.path.append('../')

from sqs_stack import SQSStack
from env import ENV


cdk_env=cdk.Environment(                     # Caylent env:
    account = os.getenv('AWS_ACCOUNT'),  # '131578276461'
    region = os.getenv('AWS_REGION')     # 'us-east-2'
)

app = cdk.App()

qldb_stack = SQSStack(
    app, "ark-sqs-stack", env=cdk_env
)

cdk.Tags.of(app).add('project', 'Ark PES')
cdk.Tags.of(app).add(ENV['MAP_TAG'], ENV['MAP_VALUE'])

app.synth()