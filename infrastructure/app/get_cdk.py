import aws_cdk as cdk

from .env import ENV


def get_lambda_function(context, code_dir: str, handler: str, name="main", **kwargs):
    """
    Returns a Lambda Function with default configs + any customizations
    passed in as parameters. Call from a CDK Stack to add a lambda function
    to the stack
    """

    return cdk.aws_lambda.Function(context, name,
            code=cdk.aws_lambda.Code.from_asset(code_dir),
            handler=handler,
            vpc=get_vpc(context),
            vpc_subnets=cdk.aws_ec2.SubnetSelection(subnets=get_subnets(context)),
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            **kwargs
        )


def get_lambda_layer(context, code_dir, name="layer", **kwargs):

    return cdk.aws_lambda.LayerVersion(
        context, name,
        code=cdk.aws_lambda.Code.from_asset(code_dir),
        compatible_runtimes=[cdk.aws_lambda.Runtime.PYTHON_3_9],
        **kwargs
    )

def get_vpc(context):

    return cdk.aws_ec2.Vpc.from_lookup(
        context, 'ark-ledger-vpc', is_default=False, vpc_id=ENV['vpc']
    )

def get_subnets(context):
    subnet_ids = ENV['subnets']

    subnets = []
    for subnet in subnet_ids:
        subnets.append(
            cdk.aws_ec2.Subnet.from_subnet_id(
                context,
                f'ark-pes-subnet-{subnet}',
                subnet
            )
        )

    return subnets
