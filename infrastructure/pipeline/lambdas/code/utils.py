import os


def get_lambda_config() -> str:
    return {
        "region": os.environ["AWS_REGION"],
        "account_id": os.environ["ACCOUNT_ID"],
        "role_arn": os.environ["CODE_BUILD_ROLE_ARN"],
        "artifact_bucket_name": os.environ["ARTIFACT_BUCKET"],
        "codebuild_name_prefix": os.environ["CODEBUILD_NAME_PREFIX"],
    }


def generate_build_spec_create_branch(branch: str, account_id: str, region: str) -> str:
    """Generates the build spec file used for the CodeBuild project"""
    return f"""version: 0.2
env:
  variables:
    BRANCH: {branch}
    DEV_ACCOUNT_ID: {account_id}
    PROD_ACCOUNT_ID: {account_id}
    REGION: {region}
  parameter-store:
      AWS_CODEBUILD_USER_ACCESS_KEY: CAYLENT_CODEBUILD_USER_ACCESSKEY
      AWS_CODEBUILD_USER_SECRET_KEY: CAYLENT_CODEBUILD_USER_SECRETKEY
phases:
  pre_build:
    commands:
      - npm install -g aws-cdk && pip install -r requirements.txt && pip install -r requirements-dev.txt
      - ./infrastructure/scripts/build.sh
      - aws configure set aws_secret_access_key $AWS_CODEBUILD_USER_SECRET_KEY
      - aws configure set aws_access_key_id $AWS_CODEBUILD_USER_ACCESS_KEY
      - aws configure set region $REGION
      - export AWS_ACCOUNT=$DEV_ACCOUNT_ID
  build:
    commands:
      - BRANCH_FORMATTED=$(echo "$BRANCH" | sed 's/_//g')
      - BRANCH_FORMATTED=$(echo "$BRANCH_FORMATTED" | sed 's/\///g')
      - export DEPLOYMENT_ENV=$BRANCH_FORMATTED
      - cdk deploy --app "python3 infrastructure/app.py" --all --require-approval never
artifacts:
  files:
    - '**/*'"""


def generate_build_spec_update_branch(branch: str, account_id: str, region: str) -> str:
    """Generates the build spec file used for the CodeBuild project"""
    return f"""version: 0.2
env:
  variables:
    BRANCH: {branch}
    DEV_ACCOUNT_ID: {account_id}
    PROD_ACCOUNT_ID: {account_id}
    REGION: {region}
  parameter-store:
      AWS_CODEBUILD_USER_ACCESS_KEY: CAYLENT_CODEBUILD_USER_ACCESSKEY
      AWS_CODEBUILD_USER_SECRET_KEY: CAYLENT_CODEBUILD_USER_SECRETKEY
phases:
  pre_build:
    commands:
      - npm install -g aws-cdk && pip install -r requirements.txt && pip install -r requirements-dev.txt
      - ./infrastructure/scripts/build.sh
      - aws configure set aws_secret_access_key $AWS_CODEBUILD_USER_SECRET_KEY
      - aws configure set aws_access_key_id $AWS_CODEBUILD_USER_ACCESS_KEY
  build:
    commands:
      - pytest --cov=infrastructure --cov=app tests
      - cd infrastructure/scripts
      - ./check_pylint.sh
      - ./check_cdk.sh
artifacts:
  files:
    - '**/*'"""


def generate_build_spec_destroy_branch(branch: str, account_id: str, region: str, artifact_bucket_name: str) -> str:
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
    build:
        commands:
            - BRANCH_FORMATTED=$(echo "$BRANCH" | sed 's/_//g')
            - BRANCH_FORMATTED=$(echo "$BRANCH_FORMATTED" | sed 's/\///g')
            - export DEPLOYMENT_ENV=$BRANCH_FORMATTED
            - cdk destroy --app "python3 infrastructure/app.py" --all --force --require-approval never
            - aws s3 rm s3://{artifact_bucket_name}/{branch} --recursive
    """


def get_codebuild_project_name(codebuild_name_prefix, branch, suffix):
    branch_formatted = branch.replace("/", "")
    project_name = f"{codebuild_name_prefix}-{branch_formatted}-{suffix}"
    return project_name
