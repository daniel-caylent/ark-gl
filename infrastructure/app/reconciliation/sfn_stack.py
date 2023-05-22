import aws_cdk as cdk
from constructs import Construct
import sys
import os

# setting path
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from app.base_stack import BaseStack
from app.utils import get_stack_prefix

# sys.path.append('../')
from env import ENV


class StepFunctionStack(BaseStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        accounts_reconciliation_lambda: cdk.aws_lambda.Function,
        ledgers_reconciliation_lambda: cdk.aws_lambda.Function,
        journals_loadbalancer_lambda: cdk.aws_lambda.Function,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        cron_hour = ENV["reconciliation_trigger_hour"]
        cron_minute = ENV["reconciliation_trigger_minute"]

        accounts_recon_task = cdk.aws_stepfunctions_tasks.LambdaInvoke(
            self,
            get_stack_prefix() + "ark-acc-recon-task",
            lambda_function=accounts_reconciliation_lambda,
            output_path="$.Payload",
        )
        ledgers_recon_task = cdk.aws_stepfunctions_tasks.LambdaInvoke(
            self,
            get_stack_prefix() + "ark-ledg-recon-task",
            lambda_function=ledgers_reconciliation_lambda,
            output_path="$.Payload",
        )
        je_lb_recon_task = cdk.aws_stepfunctions_tasks.LambdaInvoke(
            self,
            get_stack_prefix() + "ark-je-loadbalancer-task",
            lambda_function=journals_loadbalancer_lambda,
            output_path="$.Payload",
        )

        sfn_definition = accounts_recon_task.next(ledgers_recon_task).next(
            je_lb_recon_task
        )

        state_machine = cdk.aws_stepfunctions.StateMachine(
            self,
            get_stack_prefix() + "ark-reconciliation-sfn",
            state_machine_name=get_stack_prefix() + "ark-reconciliation-sfn",
            definition=sfn_definition,
        )

        eventbridge_cron = cdk.aws_events.Rule(
            self,
            get_stack_prefix() + "ark-reconciliation-trigger",
            schedule=cdk.aws_events.Schedule.cron(minute=str(cron_minute), hour=str(cron_hour)),
            rule_name=get_stack_prefix() + "ark-reconciliation-trigger",
        )

        # Add statemachine to CW Event Rule
        eventbridge_cron.add_target(
            cdk.aws_events_targets.SfnStateMachine(state_machine)
        )

        cdk.CfnOutput(
            self,
            "step-function-reconciliation",
            value=state_machine.state_machine_name,
            export_name=self.STACK_PREFIX + "step-function-name",
        )
