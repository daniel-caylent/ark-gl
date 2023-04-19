from pathlib import PurePath

from constructs import Construct
import aws_cdk as cdk

from ..get_cdk import get_lambda_function
from ..layers import get_models_layer, get_pymysql_layer, get_shared_layer
from ..utils import APP_DIR


CODE_DIR = str(PurePath(APP_DIR, 'accounts', 'get'))
MODELS_DIR = str(PurePath(APP_DIR, 'accounts', 'models'))

class AccountsGetStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)
        models_layer = get_models_layer(self, MODELS_DIR)

        func = get_lambda_function(self, CODE_DIR,
            handler="get.handler",
            layers=[shared_layer, pymysql_layer, models_layer],
            description="accounts get"
        )
