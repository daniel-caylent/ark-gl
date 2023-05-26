import os

import aws_cdk as cdk

from env import ENV

from app.dr import DRStack, LambdaRestoreStack
from app.vpc_stack import VpcStack



cdk_env=cdk.Environment(                     # Caylent env:
    account = os.getenv('AWS_ACCOUNT'),  # '131578276461'
    region = os.getenv('AWS_REGION')     # 'us-east-2'
)

app = cdk.App()
vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=cdk_env)

dr_stack = DRStack(
    app, "ark-disaster-recovery-stack", env=cdk_env
)
dr_stack.add_dependency(vpc_stack)

restore_stack = LambdaRestoreStack(
    app, "ark-restore-stack",
    bucket=dr_stack.source_bucket,
    queue=dr_stack.queue,
    env=cdk_env
)
restore_stack.add_dependency(vpc_stack)

cdk.Tags.of(app).add('project', 'Ark PES')
cdk.Tags.of(app).add(ENV['MAP_TAG'], ENV['MAP_VALUE'])

app.synth()
