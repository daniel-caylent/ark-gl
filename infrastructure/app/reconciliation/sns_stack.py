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

class SNSStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        topic = cdk.aws_sns.Topic(self, id="ark-sns-reconciliation", display_name=self.STACK_PREFIX + ENV['sns_name'])
        

        

        cdk.CfnOutput(
            self, "sns_reconciliation",
            value=topic.topic_name,
            export_name= self.STACK_PREFIX + ENV['sns_name']
        )