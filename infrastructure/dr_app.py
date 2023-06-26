import os

import aws_cdk as cdk

from env import ENV

from app.dr import DRStack, LambdaRestoreStack, ReplicationStack
from shared.vpc_stack import VpcStack
from shared.vpc_replica_stack import VpcReplicaStack
from qldb.qldb_stack import QldbStack
from qldb.lambda_stack import LambdaTriggerStack


cdk_env = cdk.Environment(
    account=os.getenv("AWS_ACCOUNT"),
    region=os.getenv("AWS_REGION"),
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

    vpc_replica_stack = VpcReplicaStack(app, "ark-gl-vpc-replica-stack", env=replication_env)

    qldb_replica_stack = QldbStack(app, "ark-gl-qldb-replica-stack", env=replication_env)
    lambda_replica_stack = LambdaTriggerStack(app, "ark-gl-lambda-trigger-replica-stack", is_replication=True, env=replication_env)
    lambda_replica_stack.add_dependency(qldb_replica_stack)
    lambda_replica_stack.add_dependency(vpc_replica_stack)
    
    replication_stack = ReplicationStack(
        app,
        "ark-dr-replication-stack",
        source_bucket=dr_stack.source_bucket,
        env=replication_env,
    )

    restore_stack = LambdaRestoreStack(
        app,
        "ark-restore-stack",
        bucket=replication_stack.replica_bucket,
        env=replication_env,
    )
    restore_stack.add_dependency(vpc_replica_stack)

cdk.Tags.of(app).add("project", "Ark PES")
cdk.Tags.of(app).add(ENV["MAP_TAG"], ENV["MAP_VALUE"])

app.synth()
