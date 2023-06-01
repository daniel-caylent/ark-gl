import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('codebuild')
region = os.environ['AWS_REGION']
role_arn = os.environ['CODE_BUILD_ROLE_ARN']
account_id = os.environ['ACCOUNT_ID']
artifact_bucket_name = os.environ['ARTIFACT_BUCKET']
codebuild_name_prefix = os.environ['CODEBUILD_NAME_PREFIX']
dev_stage_name = os.environ['DEV_STAGE_NAME']


def generate_build_spec(branch):
    return f"""version: 0.2
env:
  variables:
    BRANCH: {branch}
    DEV_ACCOUNT_ID: {account_id}
    PROD_ACCOUNT_ID: {account_id}
    REGION: {region}
phases:
  pre_build:
    commands:
      - npm install -g aws-cdk && pip install -r requirements.txt
      """ # TODO: to be done


def handler(event, context):
    logger.info(event)
    reference_type = event['detail']['referenceType']

    try:
        if reference_type == 'branch':
            branch = event['detail']['referenceName']

            # TODO to be done
    except Exception as e:
        logger.error(e)
        logger.error(e)
