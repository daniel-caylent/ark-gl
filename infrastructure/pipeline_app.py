#!/usr/bin/env python3
import os

import aws_cdk as cdk

from env import ENV

from pipeline import PipelineStack


cdk_env=cdk.Environment(                     # Caylent env:
    account = os.getenv('AWS_ACCOUNT'),  # '131578276461'
    region = os.getenv('AWS_REGION')     # 'us-east-2'
)

app = cdk.App()

PipelineStack(app, "ark-gl-pipeline-stack")

cdk.Tags.of(app).add('project', 'Ark PES')
cdk.Tags.of(app).add(ENV['MAP_TAG'], ENV['MAP_VALUE'])

app.synth()