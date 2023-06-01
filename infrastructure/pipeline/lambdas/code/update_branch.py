"""
Lambda function code used to create a CodeBuild project which deploys the CDK pipeline stack for the branch.
"""
import logging
from operator import itemgetter

import boto3

from utils import get_lambda_config, get_codebuild_project_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('codebuild')

def handler(event, context):
    """Lambda function handler"""
    logger.info(event)

    lambda_config = get_lambda_config()

    logger.info(lambda_config)

    reference_type = event['detail']['referenceType']

    codebuild_name_prefix  = \
        itemgetter(
            "codebuild_name_prefix",
        )(lambda_config)

    try:
        if reference_type == 'branch':
            branch = event['detail']['referenceName']
            project_name = get_codebuild_project_name(codebuild_name_prefix, branch)

            client.start_build(
                projectName=project_name
            )
    except Exception as e:
        logger.error(e)
