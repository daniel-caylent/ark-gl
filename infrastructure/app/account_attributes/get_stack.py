from pathlib import Path, PurePath

from constructs import Construct

from ..base_stack import BaseStack
from ..get_cdk import get_lambda_function
from ..layers import get_shared_layer, get_pymysql_layer
from ..utils import ACCOUNTS_ATTR_DIR

CODE_DIR = str(PurePath(ACCOUNTS_ATTR_DIR, 'get'))

class AccountAttributesGetStack(BaseStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)
        pymysql_layer = get_pymysql_layer(self)

        func = get_lambda_function(
            self, CODE_DIR, "get.handler",
            layers=[shared_layer, pymysql_layer],
            description="account attributes get"
        )
