import json
from datetime import datetime

from pathlib import Path, PurePath

from aws_cdk import RemovalPolicy
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_events_targets import LambdaFunction
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_s3 import BucketEncryption
from constructs import Construct
from aws_cdk.aws_iam import Role, PolicyStatement, ManagedPolicy, ServicePrincipal

from pipeline.resources.standard_bucket import S3Construct
from pipeline.stacks.iam_stack import IAMPipelineStack
from shared.base_stack import BaseStack

from aws_cdk.custom_resources import (
    AwsCustomResource,
    AwsSdkCall,
    PhysicalResourceId,
    AwsCustomResourcePolicy
)


class DefaultPipelineStack(BaseStack):
    def __init__(
        self, scope: Construct, construct_id: str, config: object, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        THIS_DIRECTORY = Path(__file__).parent.absolute()

        codebuild_prefix = config["codebuild_prefix"]
        region = config["region"]
        repo_name = config["repository_name"]

        repo = Repository.from_repository_name(
            self, self.STACK_PREFIX + "ark-ledger-repo", repo_name
        )

        args = dict(
            encryption=BucketEncryption.KMS_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
        )
        artifact_bucket = S3Construct(
            self, self.STACK_PREFIX + "ark-gl-pipeline-artifacts", args
        ).bucket

        iam_stack = IAMPipelineStack(
            self,
            self.STACK_PREFIX + "ark-gl-iam-pipeline-stack",
            account=config['dev_account_id'],
            region=region,
            repo_name=repo_name,
            artifact_bucket_arn=artifact_bucket.bucket_arn,
            codebuild_prefix=codebuild_prefix,
        )

        LAMBDA_DIR = Code.from_asset(
            str(PurePath(THIS_DIRECTORY.parent, "lambdas", "code"))
        )

        environment = {
            "DEV_ACCOUNT_ID": config['dev_account_id'],
            "QA_ACCOUNT_ID": config['qa_account_id'],
            "PROD_ACCOUNT_ID": config['prod_account_id'],
            "QA_ROLE_ARN": config['qa_role_arn'],
            "PROD_ROLE_ARN": config['prod_role_arn'],
            "CODE_BUILD_ROLE_ARN": iam_stack.code_build_role.role_arn,
            "ARTIFACT_BUCKET": artifact_bucket.bucket_name,
            "CODEBUILD_NAME_PREFIX": codebuild_prefix,
        }

        self.register_on_reference_created(LAMBDA_DIR, environment, iam_stack, repo)

        self.register_on_reference_deleted(LAMBDA_DIR, environment, iam_stack, repo)

        self.register_on_pull_request_state_change(LAMBDA_DIR, environment, iam_stack, repo)


    def register_on_pull_request_state_change(self, LAMBDA_DIR, environment, iam_stack, repo):
        on_pull_request_state_change_func = Function(
            self,
            self.STACK_PREFIX + "ark-gl-lambda-on-pull-request-state-change",
            runtime=Runtime.PYTHON_3_9,
            function_name=self.STACK_PREFIX + "ark-gl-lambda-on-pull-request-state-change",
            handler="on_pull_request_state_change.handler",
            role=iam_stack.repo_events_role,
            environment=environment,
            code=LAMBDA_DIR,
        )
        repo.on_pull_request_state_change(
            self.STACK_PREFIX + "ark-gl-repo-on_pull_request_state_change",
            description="AWS CodeCommit Pull Request Events",
            target=LambdaFunction(on_pull_request_state_change_func),
        )


    def register_on_reference_deleted(self, LAMBDA_DIR, environment, iam_stack, repo):
        on_reference_deleted_func = Function(
            self,
            self.STACK_PREFIX + "ark-gl-lambda-on-reference-deleted",
            runtime=Runtime.PYTHON_3_9,
            function_name=self.STACK_PREFIX + "ark-gl-lambda-on-reference-deleted",
            handler="on_reference_deleted.handler",
            role=iam_stack.repo_events_role,
            environment=environment,
            code=LAMBDA_DIR,
        )
        repo.on_reference_deleted(
            self.STACK_PREFIX + "ark-gl-repo-on_reference_deleted",
            description="AWS CodeCommit On Reference Deleted",
            target=LambdaFunction(on_reference_deleted_func),
        )

    def register_on_reference_created(self, LAMBDA_DIR, environment, iam_stack, repo):
        on_reference_created_func = Function(
            self,
            self.STACK_PREFIX + "ark-gl-lambda-on-reference-created",
            runtime=Runtime.PYTHON_3_9,
            function_name=self.STACK_PREFIX + "ark-gl-lambda-on-reference-created",
            handler="on_reference_created.handler",
            code=LAMBDA_DIR,
            environment=environment,
            role=iam_stack.repo_events_role,
        )

        repo.on_reference_created(
            self.STACK_PREFIX + "ark-gl-repo-on_reference_created",
            description="AWS CodeCommit On Reference Created",
            target=LambdaFunction(on_reference_created_func),
        )

        self.trigger_dev_deployment_build_creation(on_reference_created_func)

    def trigger_dev_deployment_build_creation(self, on_reference_created_func):

        payload = {
            "detail": {
                "event": "referenceCreated",
                "referenceName": "dev",
                "referenceType": "dev",
                "repositoryName": "ark-ledger",
                "referenceFullName": "refs/heads/dev"
            }
        }

        sdk_call = AwsSdkCall(
            action='invoke',
            service='Lambda',
            parameters={
                'FunctionName': on_reference_created_func.function_name,
                'InvocationType': 'RequestResponse',
                'Payload': json.dumps(payload)
            },
            physical_resource_id=PhysicalResourceId.of('MyLambdaInvocation')
        )
        exec_role = Role(
            self,
            "ark-gl-pipeline-custom-resource-execution-role",
            assumed_by=ServicePrincipal("lambda.amazonaws.com"),
        )
        exec_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )
        exec_role.add_to_policy(
            PolicyStatement(
                actions=["lambda:InvokeFunction"],
                resources=[on_reference_created_func.function_arn],
            )
        )
        AwsCustomResource(
            self, 'CustomResource' + datetime.now().isoformat(),
            role=exec_role,
            on_create=sdk_call,
            policy=AwsCustomResourcePolicy.from_sdk_calls(resources=AwsCustomResourcePolicy.ANY_RESOURCE)
        )
