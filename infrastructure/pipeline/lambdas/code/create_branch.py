"""
Lambda function code used to create a CodeBuild project which deploys the CDK pipeline stack for the branch.
"""
import logging
from operator import itemgetter

import boto3

from utils import generate_build_spec_create_branch, get_lambda_config, get_codebuild_project_name

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
        if event["detail"]["event"] == "referenceCreated" and \
            event["detail"]["referenceType"] == "branch":

            branch = event["detail"]["referenceName"]
            repo_name = event["detail"]["repositoryName"]

            project_name = get_codebuild_project_name(codebuild_name_prefix, branch, "create")

            client.create_project(
                name=project_name,
                description="Build project to deploy branch pipeline",
                source={
                    "type": "CODECOMMIT",
                    "location": f"https://git-codecommit.{region}.amazonaws.com/v1/repos/{repo_name}",
                    "buildspec": generate_build_spec_create_branch(
                        branch, account_id, region
                    ),
                },
                sourceVersion=f"refs/heads/{branch}",
                artifacts={
                    "type": "S3",
                    "location": artifact_bucket_name,
                    "path": branch,
                    "packaging": "NONE",
                    "artifactIdentifier": "BranchBuildArtifact",
                },
                environment={
                    "type": "LINUX_CONTAINER",
                    "image": "aws/codebuild/standard:6.0",
                    "computeType": "BUILD_GENERAL1_SMALL",
                },
                serviceRole=role_arn,
            )

            client.start_build(projectName=project_name)
    except Exception as e:
        logger.error(e)
