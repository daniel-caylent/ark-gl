        
from constructs import Construct

from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from aws_cdk import Duration
from shared.base_stack import BaseStack
from shared.utils import get_stack_prefix

from env import ENV


class ReplicationStack(BaseStack):
    def __init__(self, scope: Construct, id: str, source_bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        replica_conf = ENV.get("replication_configuration")
        destination_bucket_aws_account_id = replica_conf.get("account", None)
        compliance_days = replica_conf.get("compliance_duration_days")
        compliance_conf = s3.ObjectLockRetention.compliance(Duration.days(compliance_days)) if compliance_days else None

        # S3 CROSS-REGION REPLICATION
        # Create the destination bucket in the replica region
        replica_bucket_name = get_stack_prefix() + 'arkgl-dr-replica'
        replica_bucket = s3.Bucket(
           self,
           'arkgl-dr-replica-bucket',
           bucket_name=replica_bucket_name,
           encryption=s3.BucketEncryption.S3_MANAGED,
           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
           versioned=True,
           enforce_ssl=True,
           object_lock_default_retention=compliance_conf
        )

        # Give permissions to the SOURCE bucket
        replication_role = iam.Role(
            self,
            "arkgl-dr-replication-role",
            role_name=get_stack_prefix() + 'arkgl-dr-replication-role',
            assumed_by=iam.ServicePrincipal("s3.amazonaws.com"),
            path="/service-role/",
        )

        replication_role.add_to_policy(
            iam.PolicyStatement(
                resources=[source_bucket.bucket_arn],
                actions=["s3:GetReplicationConfiguration", "s3:ListBucket"],
            )
        )

        replication_role.add_to_policy(
            iam.PolicyStatement(
                resources=[source_bucket.arn_for_objects("*")],
                actions=[
                    "s3:GetObjectVersion",
                    "s3:GetObjectVersionAcl",
                    "s3:GetObjectVersionForReplication",
                    "s3:GetObjectLegalHold",
                    "s3:GetObjectVersionTagging",
                    "s3:GetObjectRetention",
                ],
            )
        )

        replication_role.add_to_policy(
            iam.PolicyStatement(
                resources=[replica_bucket.arn_for_objects("*")],
                actions=[
                    "s3:ReplicateObject",
                    "s3:ReplicateDelete",
                    "s3:ReplicateTags",
                    "s3:GetObjectVersionTagging",
                    "s3:ObjectOwnerOverrideToBucketOwner",
                ],
            )
        )

        source_bucket.node.default_child.replication_configuration = s3.CfnBucket.ReplicationConfigurationProperty(
            role=replication_role.role_arn,
            rules=[
                s3.CfnBucket.ReplicationRuleProperty(
                    destination=s3.CfnBucket.ReplicationDestinationProperty(
                        bucket=replica_bucket.bucket_arn,
                        account=destination_bucket_aws_account_id,
                    ),
                    status="Enabled"
                )
            ],
        )
