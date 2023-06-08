import os

import aws_cdk as cdk

from env import ENV

from qldb.qldb_stack import QldbStack
from qldb.lambda_stack import LambdaTriggerStack


cdk_env = cdk.Environment(  # Caylent env:
    account=os.getenv("AWS_ACCOUNT"),  # '131578276461'
    region=os.getenv("AWS_REGION"),  # 'us-east-2'
)

app = cdk.App()

qldb_stack = QldbStack(app, "ark-gl-qldb-stack", env=cdk_env)

lambda_stack = LambdaTriggerStack(app, "ark-gl-lambda-trigger-stack", env=cdk_env)
lambda_stack.add_dependency(qldb_stack)

cdk.Tags.of(app).add("project", "Ark PES")
cdk.Tags.of(app).add(ENV["MAP_TAG"], ENV["MAP_VALUE"])

app.synth()
