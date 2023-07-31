from pathlib import PurePath

from shared.get_cdk import build_lambda_layer, get_lambda_layer_from_arn

from shared.utils import LAYERS_DIR, LOCAL_LAYERS_DIR


def get_shared_layer(context):
    dir = str(PurePath(LAYERS_DIR, "shared"))

    return build_lambda_layer(
        context,
        dir,
        "shared",
        description="Lambda layer with code responses, logging, and error handling",
    )

def get_journal_entries_shared_layer(context):
    dir = str(PurePath(LAYERS_DIR, "journal_entries_shared"))

    return build_lambda_layer(
        context,
        dir,
        "journal_entries_shared",
        description="Lambda layer with shared modules for Journal Entries",
    )

def get_database_layer(context):
    dir = str(PurePath(LAYERS_DIR, "database"))

    return build_lambda_layer(
        context, dir, "database", description="Lambda layer with database integrations"
    )


def get_qldb_layer(context):
    dir = str(PurePath(LAYERS_DIR, "qldb"))

    return build_lambda_layer(
        context, dir, "qldb", description="Lambda layer with qldb integrations"
    )


def get_pymysql_layer(context):
    dir = str(PurePath(LOCAL_LAYERS_DIR, "pymysql"))

    return build_lambda_layer(
        context, dir, "pymysql", description="Lambda layer with pymysql connector"
    )


def get_pyqldb_layer(context):
    dir = str(PurePath(LOCAL_LAYERS_DIR, "pyqldb"))

    return build_lambda_layer(
        context, dir, "pyqldb", description="Lambda layer with qldb requirements"
    )


def get_models_layer(context, models_dir):
    return build_lambda_layer(
        context,
        models_dir,
        "models",
        description="Lambda layer with account api models",
    )


def get_awswrangler_layer(context, region):
    arn = "arn:aws:lambda:"+region+":336392948345:layer:AWSSDKPandas-Python39:7"

    return get_lambda_layer_from_arn(context, "layer" + arn, arn)
