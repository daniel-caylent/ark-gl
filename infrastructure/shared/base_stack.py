from aws_cdk import Stack
from constructs import Construct

from .utils import get_stack_id, get_stack_prefix


class BaseStack(Stack):
    STACK_PREFIX = ""

    def __init__(
        self, scope: Construct | None = None, id: str | None = None, **kwargs
    ) -> None:
        self.STACK_PREFIX = get_stack_prefix()
        id = get_stack_id(id)
        super().__init__(scope, id, **kwargs)
