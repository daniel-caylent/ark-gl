import aws_cdk as cdk
from constructs import Construct

from .base_stack import BaseStack
from .get_cdk import get_vpc

class VpcStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        vpc = get_vpc(self)
  
        security_group = cdk.aws_ec2.SecurityGroup(
            self, "ark-lambda-security-group",
            vpc=vpc,
            allow_all_outbound=True,
        )

        security_group.add_ingress_rule(
            cdk.aws_ec2.Peer.any_ipv4(),
            cdk.aws_ec2.Port.all_traffic(),
            "allow inbound traffic", True
        )

        vpc.add_interface_endpoint(
            "secrets-manager-endpoint",
            service=cdk.aws_ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
            security_groups=[security_group]
        )

        vpc.add_interface_endpoint(
            "aurora-endpoint",
            service=cdk.aws_ec2.InterfaceVpcEndpointAwsService.RDS,
            security_groups=[security_group]
        )

        cdk.CfnOutput(
            self, "lambdaSecurityGroupId",
            value=security_group.security_group_id,
            export_name= "lambdaSecurityGroupId"
        )
