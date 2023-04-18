from pathlib import Path, PurePath
import aws_cdk as cdk

THIS_DIRECTORY = Path(__file__).parent.absolute()

LAYERS_DIR = str(PurePath(THIS_DIRECTORY.parent, 'layers'))

def get_shared_layer(context):
    dir = str(PurePath(LAYERS_DIR, 'shared'))
    
    return cdk.aws_lambda.LayerVersion(context, "shared",
        code=cdk.aws_lambda.Code.from_asset(dir),
        compatible_runtimes=[cdk.aws_lambda.Runtime.PYTHON_3_9],
        description="Lambda layer with code responses, logging, and error handling"
    )
