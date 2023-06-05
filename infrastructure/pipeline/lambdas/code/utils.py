import os


def get_lambda_config() -> str:
    return {
        "region": os.environ['AWS_REGION'],
        "account_id": os.environ['ACCOUNT_ID'],
        "role_arn": os.environ['CODE_BUILD_ROLE_ARN'],
        "artifact_bucket_name": os.environ['ARTIFACT_BUCKET'],
        "codebuild_name_prefix": os.environ['CODEBUILD_NAME_PREFIX']
    }


def generate_build_spec(branch: str, account_id: str, region: str) -> str:
    """Generates the build spec file used for the CodeBuild project"""
    return f"""version: 0.2
env:
  variables:
    BRANCH: {branch}
    DEV_ACCOUNT_ID: {account_id}
    PROD_ACCOUNT_ID: {account_id}
    REGION: {region}
  parameter-store:
    AWS_CODEBUILD_USER_SECRET_KEY: “CAYLENT_CODEBUILD_USER_SECRET_KEY”
    AWS_CODEBUILD_USER_ACCESS_KEY: “CAYLENT_CODEBUILD_USER_ACCESS_KEY”
phases:
  pre_build:
    commands:
      - npm install -g aws-cdk && pip install -r requirements.txt && pip install -r requirements-dev.txt
      - ./infrastructure/scripts/build.sh
  build:
    commands:
      - pytest --cov=infrastructure --cov=app tests
      - aws configure set aws_access_key_id $AWS_CODEBUILD_USER_ACCESS_KEY
      - aws configure set aws_secret_access_key $AWS_CODEBUILD_USER_SECRET_KEY
      - cd infrastructure/scripts && sh synth_apps.sh
artifacts:
  files:
    - '**/*'"""


def get_codebuild_project_name(codebuild_name_prefix, branch):
    branch_formatted = branch.replace('/', '')
    project_name = f'{codebuild_name_prefix}-{branch_formatted}-create'
    return project_name