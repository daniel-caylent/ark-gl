import logging
import os

import boto3

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
        if (
            event["detail"]["isMerged"] == "True"
            and event["detail"]["pullRequestStatus"] == "Open"
        ):
            pass

        # TODO to be done
    except Exception as e:
        logger.error(e)
        logger.error(e)
