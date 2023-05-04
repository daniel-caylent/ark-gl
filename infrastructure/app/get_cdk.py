import aws_cdk as cdk

from .env import ENV


def get_lambda_function(context, code_dir: str, handler: str, name="main", env={}, **kwargs):
    """
    Returns a Lambda Function with default configs + any customizations
    passed in as parameters. Call from a CDK Stack to add a lambda function
    to the stack
    """
    vpc = get_vpc(context)
    security_group_id = cdk.Fn.import_value(context.STACK_PREFIX + 'lambdaSecurityGroup')

    security_group = cdk.aws_ec2.SecurityGroup.from_security_group_id(
        context, 'ark-lambda-security-group', security_group_id
    )

    security_group.add_ingress_rule(
        cdk.aws_ec2.Peer.any_ipv4(),
        cdk.aws_ec2.Port.all_traffic(),
        'allow inbound traffic', True
    )

    function = cdk.aws_lambda.Function(context, name,
        code=cdk.aws_lambda.Code.from_asset(code_dir),
        handler=handler,
        vpc=vpc,
        vpc_subnets=cdk.aws_ec2.SubnetSelection(subnets=get_subnets(context)),
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
        security_groups=[security_group],
        memory_size=512,
        tracing=cdk.aws_lambda.Tracing.ACTIVE, # Enabling X-Ray Tracing,
        environment={
            **ENV['deploy'],
            **env
        },
        **kwargs
    )

    # Secrets Manager permission
    secret = cdk.aws_secretsmanager.Secret.from_secret_name_v2(
        context, "db-secret", '/secret/arkgl_poc-??????'
    )

    secret_policy = cdk.aws_iam.PolicyStatement(
        actions = ['secretsmanager:GetSecretValue'],
        resources = [secret.secret_arn])

    function.role.attach_inline_policy(
        cdk.aws_iam.Policy(
            context,
            f'{name}-ark-db-secret-policy',
            policy_name = f'{name}-ark-db-secret-policy',
            statements = [secret_policy]
        )
    )

    return function


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

