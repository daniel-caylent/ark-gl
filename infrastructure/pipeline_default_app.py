#!/usr/bin/env python3
import os

import aws_cdk as cdk

from env import ENV

from pipeline.stacks.pipeline_default import DefaultPipelineStack


cdk_env = cdk.Environment(  # Caylent env:
    account=os.getenv("AWS_ACCOUNT"),  # '131578276461'
    region=os.getenv("AWS_REGION"),  # 'us-east-2'
)

app = cdk.App()

config = {
    "dev_account_id": "319244063014",
    "prod_account_id": "319244063014",
    "branch": "main",
    "default_branch": "main",
    "region": "us-east-1",
    "codebuild_prefix": "ark-gl-codebuild-pr",
    "repository_name": "ark-ledger",
}

DefaultPipelineStack(app, f"ark-gl-default-pipeline", config, env=cdk_env)

cdk.Tags.of(app).add("project", "Ark PES")
cdk.Tags.of(app).add(ENV["MAP_TAG"], ENV["MAP_VALUE"])

app.synth()