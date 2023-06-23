"""
Lambda function code used to create a CodeBuild project which deploys the CDK pipeline stack for the branch.
"""
import logging
from operator import itemgetter

import boto3

from utils import(
    generate_build_spec_create_branch,
    generate_build_spec_deploy,
    get_lambda_config,
    get_codebuild_project_name
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client("codebuild")


def handler(event, context):
    logger.info(event)

    lambda_config = get_lambda_config()

    logger.info(lambda_config)

    (
        region,
        dev_account_id,
        qa_account_id,
        prod_account_id,
        deploy_qa_role_arn,
        deploy_prod_role_arn,
        role_arn,
        artifact_bucket_name,
        codebuild_name_prefix
    ) = itemgetter(
        "region",
        "dev_account_id",
        "qa_account_id",
        "prod_account_id",
        "deploy_qa_role_arn",
        "deploy_prod_role_arn",
        "role_arn",
        "artifact_bucket_name",
        "codebuild_name_prefix"
    )(
        lambda_config
    )

    if event["detail"]["event"] == "referenceCreated":

        if event["detail"]["referenceType"] == "branch" and \
            not event["detail"]["referenceName"].startswith("rc-"):

            branch = event["detail"]["referenceName"]
            branch_lower = branch.lower()

            repo_name = event["detail"]["repositoryName"]

            project_name = get_codebuild_project_name(codebuild_name_prefix, branch_lower, "create")

            client.create_project(
                name=project_name,
                description="Build project to deploy the infrastructure",
                source={
                    "type": "CODECOMMIT",
                    "location": f"https://git-codecommit.{region}.amazonaws.com/v1/repos/{repo_name}",
                    "buildspec": generate_build_spec_create_branch(
                        branch_lower, dev_account_id, region
                    ),
                },
                sourceVersion=f"refs/heads/{branch}",
                artifacts={
                    "type": "S3",
                    "location": artifact_bucket_name,
                    "path": branch_lower,
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

        if event["detail"]["referenceType"] in ["tag", "dev"] or \
            (event["detail"]["referenceType"] == "branch" and \
             event["detail"]["referenceName"].startswith("rc-")):

            ref = event["detail"]["referenceName"]
            ref_lower = ref.lower()

            if event["detail"]["referenceType"] == "tag":
                description = f" to PROD from the {ref} tag"
                deployment_role_arn = deploy_prod_role_arn
                env = 'prod'
                account_id = prod_account_id
            elif event["detail"]["referenceType"] == "branch" and \
                 event["detail"]["referenceName"].startswith("rc-"):
                description = f" to QA from the {ref} branch"
                deployment_role_arn = deploy_qa_role_arn
                env = 'qa'
                account_id = qa_account_id
            else:
                description = " to DEV from the dev branch"
                deployment_role_arn = ""
                env = 'dev'
                account_id = dev_account_id

            repo_name = event["detail"]["repositoryName"]

            project_name = get_codebuild_project_name(codebuild_name_prefix, ref_lower, "deploy")

            client.delete_project(name=project_name)

            client.create_project(
                name=project_name,
                description="Build project to deploy the infrastructure" + description,
                source={
                    "type": "CODECOMMIT",
                    "location": f"https://git-codecommit.{region}.amazonaws.com/v1/repos/{repo_name}",
                    "buildspec": generate_build_spec_deploy(
                        env, account_id, deployment_role_arn, region
                    ),
                },
                sourceVersion=event["detail"]["referenceFullName"],
                artifacts={
                    'type': 'NO_ARTIFACTS'
                },
                environment={
                    "type": "LINUX_CONTAINER",
                    "image": "aws/codebuild/standard:6.0",
                    "computeType": "BUILD_GENERAL1_SMALL",
                },
                serviceRole=role_arn,
            )
