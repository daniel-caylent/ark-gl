from os import path

from pathlib import Path, PurePath

from aws_cdk import (
    Stack, aws_codepipeline_actions, Aspects, RemovalPolicy
)
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_events_targets import LambdaFunction
from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_s3 import BucketEncryption
from aws_cdk.pipelines import CodePipeline, CodeBuildStep, CodePipelineSource, ManualApprovalStep
from cdk_nag import NagSuppressions, NagPackSuppression
from constructs import Construct

from pipeline.aspects.key_rotation_aspect import KeyRotationAspect
from pipeline.resources.standard_bucket import S3Construct
from pipeline.stacks.iam_stack import IAMPipelineStack

from app.base_stack import BaseStack


class DefaultPipelineStack(BaseStack):

    def __init__(self, scope: Construct, construct_id: str, config: object, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        THIS_DIRECTORY = Path(__file__).parent.absolute()

        codebuild_prefix = config['codebuild_prefix']
        region = config['region']
        repo_name = config['repository_name']
        branch = config['branch']
        default_branch = config['default_branch']
        dev_account_id = config['dev_account_id']
        prod_account_id = config['prod_account_id'] if branch == default_branch else dev_account_id

        repo = Repository.from_repository_name(self, self.STACK_PREFIX + 'ark-ledger-repo', repo_name)

        dev_stage_name = 'DEV'

        args = dict(
            encryption=BucketEncryption.KMS_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
        )
        artifact_bucket = S3Construct(self, self.STACK_PREFIX + 'ark-gl-pipeline-artifacts', args).bucket

        iam_stack = IAMPipelineStack(
            self,
            self.STACK_PREFIX + 'ark-gl-iam-pipeline-stack',
            account=dev_account_id,
            region=region,
            repo_name=repo_name,
            artifact_bucket_arn=artifact_bucket.bucket_arn,
            codebuild_prefix=codebuild_prefix)

        LAMBDA_DIR = Code.from_asset(str(PurePath(THIS_DIRECTORY.parent, 'lambdas', 'code')))

        environment={
            "ACCOUNT_ID": dev_account_id,
            "CODE_BUILD_ROLE_ARN": iam_stack.code_build_role.role_arn,
            "ARTIFACT_BUCKET": artifact_bucket.bucket_name,
            "CODEBUILD_NAME_PREFIX": codebuild_prefix,
            "DEV_STAGE_NAME": f'{dev_stage_name}-'
        }

        create_branch_func = Function(
            self,
            self.STACK_PREFIX + 'ark-gl-lambda-create-build',
            runtime=Runtime.PYTHON_3_9,
            function_name=self.STACK_PREFIX + 'ark-gl-lambda-create-build',
            handler='create_branch.handler',
            code=LAMBDA_DIR,
            environment=environment,
            role=iam_stack.create_branch_role)


        repo.on_reference_created(
            self.STACK_PREFIX + 'ark-gl-repo-on-reference-created',
            description="AWS CodeCommit reference created event.",
            target=LambdaFunction(create_branch_func))

        destroy_branch_func = Function(
            self,
            self.STACK_PREFIX + 'ark-gl-lambda-destroy-build',
            runtime=Runtime.PYTHON_3_9,
            function_name=self.STACK_PREFIX + 'ark-gl-lambda-destroy-build',
            handler='destroy_branch.handler',
            role=iam_stack.delete_branch_role,
            environment=environment,
            code=LAMBDA_DIR)

        repo.on_reference_deleted(
            self.STACK_PREFIX + 'ark-gl-repo-on-reference-deleted',
            description="AWS CodeCommit reference deleted event.",
            target=LambdaFunction(destroy_branch_func))

        update_branch_func = Function(
            self,
            self.STACK_PREFIX + 'ark-gl-lambda-update-build',
            runtime=Runtime.PYTHON_3_9,
            function_name=self.STACK_PREFIX + 'ark-gl-lambda-update-build',
            handler='update_branch.handler',
            role=iam_stack.delete_branch_role,
            environment=environment,
            code=LAMBDA_DIR)

        repo.on_reference_updated(
            self.STACK_PREFIX + 'ark-gl-repo-on-reference-updated',
            description="AWS CodeCommit reference updated event.",
            target=LambdaFunction(update_branch_func))
