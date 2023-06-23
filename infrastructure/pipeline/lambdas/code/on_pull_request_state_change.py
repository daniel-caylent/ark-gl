"""
Lambda function code used to create a CodeBuild project which deploys the CDK pipeline stack for the branch.
"""
import logging
import json
from operator import itemgetter

import boto3

from utils import generate_build_spec_update_branch, get_lambda_config, get_codebuild_project_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

codebuild_client = boto3.client("codebuild")

codecommit_client = boto3.client("codecommit")

SUPPORTED_EVENTS = ["pullRequestCreated", "pullRequestSourceBranchUpdated", "pullRequestStatusChanged", "pullRequestMergeStatusUpdated"]


def handler(event, context):
    """Lambda function handler"""
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

    event_name = event["detail"]["event"]

    if event_name not in SUPPORTED_EVENTS:
        print(f"{event_name} is not supported")
        return ""

    branch = event["detail"]["sourceReference"].replace("refs/heads/", "")
    branch_lower = branch.lower()

    repo_name = event["detail"]["repositoryNames"][0]
    project_name = get_codebuild_project_name(codebuild_name_prefix, branch_lower, "pr")

    if event["detail"]["event"] == "pullRequestCreated":

        pull_request_id = event["detail"]["pullRequestId"]
        revision_id = event["detail"]["revisionId"]

        # TODO: Enable Approval Rules
        #approval_rule_content = {
        #    "Version": "2018-11-08",
        #    "Statements": [
        #        {
        #            "Type": "Approvers",
        #            "ApprovalPoolMembers": [
        #                f'arn:aws:iam::{region}:user/caylent-codebuild-user'
        #            ],
        #            "NumberOfApprovalsNeeded": 1
        #        }
        #    ]
        #}

        #approval_rule_name = f'ark-gl-{branch_lower}-approval-rule'

        #response = codecommit_client.create_pull_request_approval_rule(
        #    pullRequestId=event["detail"]["pullRequestId"],
        #    approvalRuleName=f'{branch_lower}-approval-rule',
        #    approvalRuleContent=json.dumps(approval_rule_content)
        #)

        codebuild_client.create_project(
            name=project_name,
            description="Build project to test the code in the branch",
            source={
                "type": "CODECOMMIT",
                "location": f"https://git-codecommit.{region}.amazonaws.com/v1/repos/{repo_name}",
                "buildspec": generate_build_spec_update_branch(
                    branch_lower, dev_account_id, region, pull_request_id, revision_id
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
                'type': 'LINUX_CONTAINER',
                'image': 'aws/codebuild/standard:6.0',
                'computeType': 'BUILD_GENERAL1_SMALL'
            },
            serviceRole=role_arn
        )

        codebuild_client.start_build(projectName=project_name)


    elif event["detail"]["event"] == "pullRequestSourceBranchUpdated":
        codebuild_client.start_build(projectName=project_name)


    elif (
            event["detail"]["event"] == "pullRequestStatusChanged" and \
            event["detail"]["pullRequestStatus"] == "Closed"
        ) or \
        (
            event["detail"]["event"] == "pullRequestMergeStatusUpdated" and \
            event["detail"]["isMerged"] == "True"
        ):
            codebuild_client.delete_project(name=project_name)
