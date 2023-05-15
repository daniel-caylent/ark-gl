import aws_cdk as cdk
from constructs import Construct
import sys
import os
 
# setting path
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from app.base_stack import BaseStack

#sys.path.append('../')
from env import ENV

class SQSStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # An sqs queue for unsuccessful invocations of a lambda function

        dead_letter_queue = cdk.aws_sqs.Queue(self, id="ark-sqs-reconciliation", 
                                              queue_name=self.STACK_PREFIX +"ark-sqs-reconciliation")
        

        

       # cdk.CfnOutput(
       #     self, "qldbLedger",
       #     value=ledger.name,
       #     export_name= self.STACK_PREFIX + "qldbLedger"
       # )
