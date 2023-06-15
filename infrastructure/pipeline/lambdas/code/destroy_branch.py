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
        account_id,
        region,
    ) = itemgetter(
        "codebuild_name_prefix",
        "artifact_bucket_name",
        "role_arn",
        "account_id",
        "region",
    )(
        lambda_config
    )

    try:
        reference_type = event['detail']['referenceType']

        if (reference_type == "branch"):

            branch = event["detail"]["referenceName"]

            repository_name = event['detail']["repositoryName"]

            destroy_code_build_project_name = get_codebuild_project_name(codebuild_name_prefix, branch, "destroy")
            create_code_build_project_name = get_codebuild_project_name(codebuild_name_prefix, branch, "create")

            client.create_project(
                name=destroy_code_build_project_name,
                description="Build project to destroy branch resources",
                source={
                    'type': 'S3',
                    "location": f"{artifact_bucket_name}/{branch}/{create_code_build_project_name}/",
                    'buildspec': generate_build_spec_destroy_branch(
                        branch,
                        account_id,
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

    except Exception as e:
        logger.error(e)
