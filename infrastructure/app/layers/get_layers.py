from pathlib import PurePath

from ..get_cdk import get_lambda_layer

from ..utils import LAYERS_DIR, LOCAL_LAYERS_DIR

def get_shared_layer(context):
    dir = str(PurePath(LAYERS_DIR, 'shared'))

    return get_lambda_layer(context, dir, "shared",
        description="Lambda layer with code responses, logging, and error handling"
    )

def get_database_layer(context):
    dir = str(PurePath(LAYERS_DIR, 'database'))

    return get_lambda_layer(context, dir, "database",
        description="Lambda layer with database integrations"
    )

def get_qldb_layer(context):
    dir = str(PurePath(LAYERS_DIR, 'qldb'))

    return get_lambda_layer(context, dir, "qldb",
        description="Lambda layer with qldb integrations"
    )

def get_pymysql_layer(context):
    dir = str(PurePath(LOCAL_LAYERS_DIR, 'pymysql'))

    return get_lambda_layer(context, dir, "pymysql",
        description="Lambda layer with pymysql connector"
    )

def get_pyqldb_layer(context):
    dir = str(PurePath(LOCAL_LAYERS_DIR, 'pyqldb'))

    return get_lambda_layer(context, dir, "pyqldb",
        description="Lambda layer with qldb requirements"
    )

def get_models_layer(context, models_dir):

    return get_lambda_layer(
        context, models_dir, "models",
        description="Lambda layer with account api models"
    )
