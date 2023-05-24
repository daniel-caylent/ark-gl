import aws_cdk as cdk
from constructs import Construct
from pathlib import PurePath
import sys
import os
from ..get_cdk import build_qldb_lambda_function
from ..layers import (
    get_pymysql_layer,
    get_shared_layer,
    get_qldb_layer,
    get_pyqldb_layer,
)

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
from ..utils import DR_DIR

RESTORE_CODE_DIR = str(PurePath(DR_DIR, "restore"))


class LambdaRestoreStack(BaseStack):
    def __init__(self, scope: Construct, id: str, bucket: cdk.aws_s3.Bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        dr_bucket_name = ENV["dr_bucket_name"]
        ledger_name = ENV["ledger_name"]
        
        shared_layer = get_shared_layer(self)
        qldb_layer = get_qldb_layer(self)
        qldb_reqs = get_pyqldb_layer(self)

        self.restore_function = build_qldb_lambda_function(
            self,
            RESTORE_CODE_DIR,
            handler="restore_qldb.handler",
            layers=[shared_layer, qldb_layer, qldb_reqs],
            description="dr qldb restore lambda",
            env={
                "dr_bucket_name": dr_bucket_name,
                "ledger_name": ledger_name,
                "LOG_LEVEL": "INFO",
            },
        )

        bucket.grant_read(self.restore_function.role)
