
import aws_cdk as cdk

from .utils import get_stack_prefix
from env import ENV


def build_lambda_function(
    context,
    code_dir: str,
    handler: str,
    name="main",
    env={},
    timeout=60,
    exclude=[],
    **kwargs,
):
    """
    Returns a Lambda Function with default configs + any customizations
    passed in as parameters. Call from a CDK Stack to add a lambda function
    to the stack
    """
    vpc = get_vpc(context, name)

    security_group_id = cdk.Fn.import_value(
        context.STACK_PREFIX + "lambda-security-group"
    )

    security_group = cdk.aws_ec2.SecurityGroup.from_security_group_id(
        context, f"ark-lambda-security-group-{name}", security_group_id
    )

    security_group.add_ingress_rule(
        cdk.aws_ec2.Peer.any_ipv4(),
        cdk.aws_ec2.Port.all_traffic(),
        "allow inbound traffic",
        True,
    )

    function = cdk.aws_lambda.Function(
        context,
        name,
        code=cdk.aws_lambda.Code.from_asset(code_dir, exclude=exclude),
        handler=handler,
        vpc=vpc,
        vpc_subnets=cdk.aws_ec2.SubnetSelection(subnets=get_subnets(context, name)),
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
        security_groups=[security_group],
        memory_size=512,
        timeout=cdk.Duration.seconds(timeout),
        tracing=cdk.aws_lambda.Tracing.ACTIVE,  # Enabling X-Ray Tracing,
        environment={**ENV["deploy"], **env},
        **kwargs,
    )

    # Secrets Manager permission
    secret = cdk.aws_secretsmanager.Secret.from_secret_name_v2(
        context, f"db-secret-{name}", f"{ENV['deploy']['DB_SECRET_NAME']}-??????"
    )

    secret_policy = cdk.aws_iam.PolicyStatement(
        actions=["secretsmanager:GetSecretValue"], resources=[secret.secret_arn]
    )

    function.role.attach_inline_policy(
        cdk.aws_iam.Policy(
            context,
            f"{name}-ark-db-secret-policy",
            policy_name=f"{name}-ark-db-secret-policy",
            statements=[secret_policy],
        )
    )

    return function


def build_dr_lambda_function(
    context, code_dir: str, handler: str, name="main", env={}, cdk_env={}, **kwargs
):
    function = build_lambda_function(context, code_dir, handler, name, env, **kwargs)
    role_arn = env['ROLE_ARN']
    ledger_name = ENV["deploy"]["LEDGER_NAME"]
    ledger_arn = (
        "arn:aws:qldb:"
        + cdk_env.region
        + ":"
        + cdk_env.account
        + ":ledger/"
        + ledger_name
    )

    dr_actions_statement = cdk.aws_iam.PolicyStatement(
        actions=[
            "qldb:ListJournalS3Exports",
            "qldb:ListJournalS3ExportsForLedger",
            "qldb:ExportJournalToS3",
        ],
        resources=[ledger_arn],
    )

    dr_actions_statement2 = cdk.aws_iam.PolicyStatement(
        actions=[
            "iam:PassRole",
        ],
        resources=[role_arn],
    )

    dr_policy = cdk.aws_iam.Policy(
        context,
        f"ark-dr-policy-{name}",
        policy_name="ark-dr-policy",
        statements=[dr_actions_statement, dr_actions_statement2],
    )

    function.role.attach_inline_policy(dr_policy)

    return function


def build_qldb_lambda_function(
    context, code_dir: str, handler: str, name="main", env={}, cdk_env={}, **kwargs
):
    function = build_lambda_function(context, code_dir, handler, name, env, **kwargs)

    ledger_name = ENV["deploy"]["LEDGER_NAME"]
    ledger_arn = (
        "arn:aws:qldb:"
        + cdk_env.region
        + ":"
        + cdk_env.account
        + ":ledger/"
        + ledger_name
    )

    qldb_send_command_statement = cdk.aws_iam.PolicyStatement(
        actions=["qldb:SendCommand"], resources=[ledger_arn]
    )

    qldb_actions_statement = cdk.aws_iam.PolicyStatement(
        actions=[
            "qldb:ShowCatalog",
            "qldb:PartiQLInsert",
            "qldb:ExecuteStatement",
            "qldb:PartiQLCreateTable",
            "qldb:PartiQLCreateIndex",
            "qldb:PartiQLSelect",
        ],
        resources=[ledger_arn + "/*"],
    )

    qldb_policy = cdk.aws_iam.Policy(
        context,
        f"ark-db-qldb-policy-{name}",
        policy_name="ark-db-qldb-policy",
        statements=[qldb_send_command_statement, qldb_actions_statement],
    )

    function.role.attach_inline_policy(qldb_policy)

    return function


def build_decorated_qldb_lambda_function(
    context, code_dir: str, handler: str, name="main", env={}, cdk_env={}, **kwargs
):
    function = build_qldb_lambda_function(
        context, code_dir, handler, name, env, cdk_env, **kwargs
    )

    sqs_name = ENV["sqs_name"]
    sqs_arn = (
        "arn:aws:sqs:"
        + cdk_env.region
        + ":"
        + cdk_env.account
        + ":"
        + get_stack_prefix()
        + sqs_name
    )

    sqs_actions_statement = cdk.aws_iam.PolicyStatement(
        actions=[
            "sqs:DeleteMessage",
            "sqs:ListQueues",
            "sqs:GetQueueUrl",
            "sqs:ReceiveMessage",
            "sqs:SendMessage",
            "sqs:GetQueueAttributes",
        ],
        resources=[sqs_arn],
    )

    sqs_policy = cdk.aws_iam.Policy(
        context,
        f"ark-db-sqs-policy-{name}",
        policy_name="ark-db-sqs-policy",
        statements=[sqs_actions_statement],
    )

    function.role.attach_inline_policy(sqs_policy)

    function.add_environment("SQS_NAME", sqs_name)

    return function


def build_lambda_layer(context, code_dir, name="layer", **kwargs):
    return cdk.aws_lambda.LayerVersion(
        context,
        name,
        code=cdk.aws_lambda.Code.from_asset(code_dir),
        compatible_runtimes=[cdk.aws_lambda.Runtime.PYTHON_3_9],
        **kwargs,
    )


def get_lambda_layer_from_arn(context, id, arn):
    return cdk.aws_lambda.LayerVersion.from_layer_version_arn(context, id, arn)


def build_lambda_integration(
    context, function, role_suffix: str
) -> cdk.aws_apigateway.LambdaIntegration:
    api_role = cdk.aws_iam.Role(
        context,
        f"api-role-{role_suffix}",
        role_name="api-role-" + role_suffix,
        assumed_by=cdk.aws_iam.ServicePrincipal("apigateway.amazonaws.com"),
    )
    api_role.add_to_policy(
        cdk.aws_iam.PolicyStatement(
            resources=[function.function_arn], actions=["lambda:InvokeFunction"]
        )
    )
    return cdk.aws_apigateway.LambdaIntegration(
        function, proxy=True, credentials_role=api_role
    )


def build_integration_responses(**kwargs) -> cdk.aws_apigateway.IntegrationResponse:
    return cdk.aws_apigateway.IntegrationResponse(**kwargs)


def build_method_response(**kwargs) -> cdk.aws_apigateway.MethodResponse:
    return cdk.aws_apigateway.MethodResponse(**kwargs)


def build_api_gateway(context, id: str, **kwargs) -> cdk.aws_apigateway.IRestApi:
    return cdk.aws_apigateway.RestApi(context, id, **kwargs)


def build_api_gateway_deployment(
    context, id: str, **kwargs
) -> cdk.aws_apigateway.Deployment:
    return cdk.aws_apigateway.Deployment(context, id, **kwargs)


def build_api_gateway_stage(context, id: str, **kwargs) -> cdk.aws_apigateway.Stage:
    return cdk.aws_apigateway.Stage(context, id, **kwargs)


def get_api_gateway_from_attributes(
    context, id: str, rest_api_id: str, root_resource_id: str
) -> cdk.aws_apigateway.IRestApi:
    return cdk.aws_apigateway.RestApi.from_rest_api_attributes(
        context, id, rest_api_id=rest_api_id, root_resource_id=root_resource_id
    )


def get_imported_value(shared_value_to_import: str) -> str:
    return cdk.Fn.import_value(shared_value_to_import)


def get_lambda_function_from_arn(
    context, id: str, function_arn: str
) -> cdk.aws_lambda.IFunction:
    return cdk.aws_lambda.Function.from_function_arn(context, id, function_arn)


def get_vpc(context, name=""):
    return cdk.aws_ec2.Vpc.from_lookup(
        context, f"ark-ledger-vpc-{name}", is_default=False, vpc_id=ENV["vpc"]
    )


def get_subnets(context, name=""):
    subnet_ids = ENV["subnets"]

    subnets = []
    for subnet in subnet_ids:
        subnets.append(
            cdk.aws_ec2.Subnet.from_subnet_id(
                context, f"ark-pes-subnet-{subnet}-{name}", subnet
            )
        )

    return subnets
