from pathlib import Path, PurePath

from constructs import Construct
import aws_cdk as cdk

from ..utils import get_shared_layer

THIS_DIRECTORY = Path(__file__).parent.absolute()
RUNTIME_DIR = str(PurePath(THIS_DIRECTORY, 'runtime'))
GET_DIR = str(PurePath(RUNTIME_DIR, 'get'))

class AccountsGetStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        shared_layer = get_shared_layer(self)

        func = cdk.aws_lambda.Function(self, "main",
            code=cdk.aws_lambda.Code.from_asset(GET_DIR),
            handler="get.handler",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            layers=[shared_layer],
            description="accounts get"
        )
