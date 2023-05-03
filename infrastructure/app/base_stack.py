from aws_cdk import Stack, Environment, PermissionsBoundary, IStackSynthesizer
from constructs import Construct
from typing import Dict, Any, Mapping

import os

class BaseStack(Stack):

    STACK_PREFIX = ''

    def __init__(self, scope: Construct | None = None, id: str | None = None, *, analytics_reporting: bool | None = None, cross_region_references: bool | None = None, description: str | None = None, env: Environment | Dict[str, Any] | None = None, permissions_boundary: PermissionsBoundary | None = None, stack_name: str | None = None, synthesizer: IStackSynthesizer | None = None, tags: Mapping[str, str] | None = None, termination_protection: bool | None = None) -> None:
        DEPLOYMENT_ENV = 'DEPLOYMENT_ENV'
        self.STACK_PREFIX = os.getenv(DEPLOYMENT_ENV) + '-' if os.getenv(DEPLOYMENT_ENV) is not None else ''
        id = id if id is None else self.STACK_PREFIX + id
        super().__init__(scope, id, analytics_reporting=analytics_reporting, cross_region_references=cross_region_references, description=description, env=env, permissions_boundary=permissions_boundary, stack_name=stack_name, synthesizer=synthesizer, tags=tags, termination_protection=termination_protection)