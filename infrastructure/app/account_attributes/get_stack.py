from pathlib import Path, PurePath

from constructs import Construct
import aws_cdk as cdk

from ..get_cdk import get_lambda_function
from ..layers import get_shared_layer, get_pymysql_layer
from ..utils import ACCOUNTS_ATTR_DIR

GET_DIR = str(PurePath(ACCOUNTS_ATTR_DIR, 'get'))

class AccountAttributesGetStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)

        func = get_lambda_function(
            self, GET_DIR, "get.handler",
            layers=[shared_layer, pymysql_layer],
            description="account attributes get"
        )
