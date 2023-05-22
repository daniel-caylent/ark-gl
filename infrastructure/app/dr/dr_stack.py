import aws_cdk as cdk
from constructs import Construct
import sys
import os
from aws_cdk import aws_s3 as s3

# setting path
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from app.base_stack import BaseStack
from app.utils import get_stack_prefix

# sys.path.append('../')
from env import ENV


class DRStack(BaseStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = "arkgl-dr"
        source_bucket = s3.Bucket(
            self,
            "arkgl-dr-bucket",
            bucket_name=bucket_name,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            enforce_ssl=True
        )
        # Create the destination bucket in the replica region
        #replica_region = 'us-west-2'  # Replace with your desired replica region
        #replica_bucket_name = 'arkgl-dr-replica'
        #replica_bucket = s3.Bucket(
        #    self,
        #    'arkgl-dr-replica-bucket',
        #    bucket_name=replica_bucket_name,
        #    encryption=s3.BucketEncryption.S3_MANAGED,
        #    block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        #    versioned=True,
        #    enforce_ssl=True,
        #    bucket_key_enabled=True,
        #    replication_destinations=[
        #        s3.ReplicationDestination(
        #            bucket=source_bucket,
        #            region=replica_region
        #        )
        #    ]
        #)

        # Enable compliance mode for the replica bucket
        #replica_bucket.enable_compliance_mode()
