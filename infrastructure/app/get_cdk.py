import aws_cdk as cdk

def get_lambda_function(context, code_dir, handler, name="main", **kwargs):

    return cdk.aws_lambda.Function(context, name,
            code=cdk.aws_lambda.Code.from_asset(code_dir),
            handler=handler,
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