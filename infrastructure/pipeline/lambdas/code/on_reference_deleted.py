import logging
import os
import boto3

from operator import itemgetter

from utils import  generate_build_spec_destroy_branch, get_lambda_config, get_codebuild_project_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client("codebuild")

def handler(event, context):
    logger.info(event)

    lambda_config = get_lambda_config()

    logger.info(lambda_config)

    (
        codebuild_name_prefix,
        artifact_bucket_name,
        role_arn,
        dev_account_id,
        region,
    ) = itemgetter(
        "codebuild_name_prefix",
        "artifact_bucket_name",
        "role_arn",
        "dev_account_id",
        "region",
    )(
        lambda_config
    )

    reference_type = event['detail']['referenceType']
    reference_name = event['detail']['referenceName']

    if reference_type == "branch":
        if not reference_name.startswith("rc-"):

            branch = reference_name
            branch_lower = branch.lower()

            destroy_code_build_project_name = get_codebuild_project_name(codebuild_name_prefix, branch_lower, "destroy")
            create_code_build_project_name = get_codebuild_project_name(codebuild_name_prefix, branch_lower, "create")

            client.create_project(
                name=destroy_code_build_project_name,
                description="Build project to destroy branch infrastructure",
                source={
                    'type': 'S3',
                    "location": f"{artifact_bucket_name}/{branch_lower}/{create_code_build_project_name}/",
                    'buildspec': generate_build_spec_destroy_branch(
                        branch_lower,
                        dev_account_id,
                        region,
                        artifact_bucket_name,
                        destroy_code_build_project_name,
                        create_code_build_project_name)
                },
                artifacts={
                    'type': 'NO_ARTIFACTS'
                },
                environment={
                    'type': 'LINUX_CONTAINER',
                    'image': 'aws/codebuild/standard:6.0',
                    'computeType': 'BUILD_GENERAL1_SMALL'
                },
                serviceRole=role_arn
            )

            client.start_build(
                projectName=destroy_code_build_project_name
            )
        elif reference_name.startswith("rc-"):

            branch = reference_name
            branch_lower = branch.lower()

            project_name = get_codebuild_project_name(codebuild_name_prefix, branch_lower, "deploy")

            client.delete_project(
                name=project_name
            )
