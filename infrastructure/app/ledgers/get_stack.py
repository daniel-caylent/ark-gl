from pathlib import PurePath

from constructs import Construct

from ..base_stack import BaseStack
from ..get_cdk import get_lambda_function
from ..layers import (
    get_models_layer,
    get_pymysql_layer,
    get_shared_layer,
    get_database_layer
)
from ..utils import LEDGERS_DIR


CODE_DIR = str(PurePath(LEDGERS_DIR, 'get'))
MODELS_DIR = str(PurePath(LEDGERS_DIR, 'models'))

class LedgersGetStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        models_layer = get_models_layer(self, MODELS_DIR)
        db_layer = get_database_layer(self)

        func = get_lambda_function(self, CODE_DIR,
            handler="get.handler",
            layers=[shared_layer, pymysql_layer, models_layer, db_layer],
            description="ledgers get"
        )
