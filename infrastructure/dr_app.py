import os

import aws_cdk as cdk

from env import ENV

from app.dr import DRStack, LambdaRestoreStack, ReplicationStack
from shared.vpc_stack import VpcStack


cdk_env = cdk.Environment(  # Caylent env:
    account=os.getenv("AWS_ACCOUNT"),  # '131578276461'
    region=os.getenv("AWS_REGION"),  # 'us-east-2'
)

app = cdk.App()
vpc_stack = VpcStack(app, "ark-gl-vpc-stack", env=cdk_env)

dr_stack = DRStack(app, "ark-disaster-recovery-stack", env=cdk_env, cross_region_references=True)
dr_stack.add_dependency(vpc_stack)

replica_conf = ENV.get("replication_configuration")
if replica_conf:
    replication_env = cdk.Environment(
        account=os.getenv("AWS_ACCOUNT"),
        region=replica_conf.get("region"),
    )
    replication_stack = ReplicationStack(
        app,
        "ark-dr-replication-stack",
        source_bucket=dr_stack.source_bucket,
        env=replication_env)

restore_stack = LambdaRestoreStack(
    app,
    "ark-restore-stack",
    bucket=dr_stack.source_bucket,
    queue=dr_stack.queue,
    env=cdk_env,
)
restore_stack.add_dependency(vpc_stack)

cdk.Tags.of(app).add("project", "Ark PES")
cdk.Tags.of(app).add(ENV["MAP_TAG"], ENV["MAP_VALUE"])

app.synth()
