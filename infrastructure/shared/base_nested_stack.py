import builtins
from aws_cdk import Duration, NestedStack, RemovalPolicy
from constructs import Construct
from typing import Mapping, Sequence

from .utils import get_stack_id, get_stack_prefix

class BaseNestedStack(NestedStack):

    STACK_PREFIX = ''

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        self.STACK_PREFIX = get_stack_prefix()
        id = get_stack_id(id)
        super().__init__(scope, id, **kwargs)