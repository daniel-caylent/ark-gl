from pathlib import PurePath

from .get_cdk import get_lambda_layer

from .utils import LAYERS_DIR

def get_shared_layer(context):
    dir = str(PurePath(LAYERS_DIR, 'shared'))
    
    return get_lambda_layer(context, dir, "shared",
        description="Lambda layer with code responses, logging, and error handling"
    )

def get_pymysql_layer(context):
    dir = str(PurePath(LAYERS_DIR, 'pymysql'))

    return get_lambda_layer(context, dir, "pymysql",
        description="Lambda layer with pymysql connector"
    )

def get_models_layer(context, models_dir):

    return get_lambda_layer(
        context, models_dir, "models",
        description="Lambda layer with account api models"
    )
