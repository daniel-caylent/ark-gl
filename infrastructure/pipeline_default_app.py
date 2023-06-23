#!/usr/bin/env python3
import os

import aws_cdk as cdk

from env import dev, qa, prod, map_tag

from pipeline.stacks.pipeline_default import DefaultPipelineStack


cdk_env = cdk.Environment(  # Caylent env:
    account=os.getenv("AWS_ACCOUNT"),  # '131578276461'
    region=os.getenv("AWS_REGION"),  # 'us-east-2'
)

app = cdk.App()

config = {
    "region": "us-east-1",
    "codebuild_prefix": "ark-gl-codebuild",
    "repository_name": "ark-ledger",
    "dev_account_id": dev['ACCOUNT_ID'],
    "qa_account_id": qa['ACCOUNT_ID'],
    "prod_account_id": prod['ACCOUNT_ID'],
    "qa_role_arn": qa['deploy']['ROLE_ARN'],
    "prod_role_arn": prod['deploy']['ROLE_ARN'],
}

DefaultPipelineStack(app, f"ark-gl-default-pipeline", config, env=cdk_env)

cdk.Tags.of(app).add("project", "Ark PES")
cdk.Tags.of(app).add(map_tag["MAP_TAG"], map_tag["MAP_VALUE"])

app.synth()