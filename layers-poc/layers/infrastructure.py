from pathlib import Path, PurePath

from constructs import Construct
import aws_cdk as cdk

THIS_DIRECTORY = Path(__file__).parent.absolute()
EXTERNAL_DIR = str(PurePath(THIS_DIRECTORY, 'external'))
DB_DIR = str(PurePath(THIS_DIRECTORY, 'db'))


class LambdaLayersStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the Lambda layer
        db_layer = cdk.aws_lambda.LayerVersion(self, "fastapi-db-layer",
            code=cdk.aws_lambda.Code.from_asset(DB_DIR),
            compatible_runtimes=[cdk.aws_lambda.Runtime.PYTHON_3_9],
            description="Lambda layer with database connectors"
        )

        cdk.CfnOutput(
            self, "fastapiDbLayer",
            value=db_layer.layer_version_arn,
            export_name="fastapiDbLayer"
        )

        external_layer = cdk.aws_lambda.LayerVersion(self, "fastapi-external-layer",
            code=cdk.aws_lambda.Code.from_asset(EXTERNAL_DIR),
            compatible_runtimes=[cdk.aws_lambda.Runtime.PYTHON_3_9],
            description="Lambda layer that includes fastapi and dependencies"
        )

        cdk.CfnOutput(
            self, "fastapiExternalLayer",
            value=external_layer.layer_version_arn,
            export_name="fastapiExternalLayer"
        )
