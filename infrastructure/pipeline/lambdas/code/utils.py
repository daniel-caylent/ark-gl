import os


def get_lambda_config() -> str:
    return {
        "region": os.environ["AWS_REGION"],
        "dev_account_id": os.environ["DEV_ACCOUNT_ID"],
        "qa_account_id": os.environ["QA_ACCOUNT_ID"],
        "prod_account_id": os.environ["PROD_ACCOUNT_ID"],
        "deploy_qa_role_arn": os.environ["QA_ROLE_ARN"],
        "deploy_prod_role_arn": os.environ["PROD_ROLE_ARN"],
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
    ACCOUNT_ID: {account_id}
    REGION: {region}
  parameter-store:
      AWS_CODEBUILD_USER_ACCESS_KEY: CAYLENT_CODEBUILD_USER_ACCESSKEY
      AWS_CODEBUILD_USER_SECRET_KEY: CAYLENT_CODEBUILD_USER_SECRETKEY
phases:
  pre_build:
    commands:
      - npm install -g aws-cdk && pip install -r requirements.txt
      - ./infrastructure/scripts/build.sh
      - aws configure set aws_secret_access_key $AWS_CODEBUILD_USER_SECRET_KEY
      - aws configure set aws_access_key_id $AWS_CODEBUILD_USER_ACCESS_KEY
      - aws configure set region $REGION
      - export AWS_ACCOUNT=$ACCOUNT_ID
      - BRANCH_FORMATTED=$(echo "$BRANCH" | sed 's/_//g')
      - BRANCH_FORMATTED=$(echo "$BRANCH_FORMATTED" | sed 's/\///g')
      - export DEPLOYMENT_ENV=$BRANCH_FORMATTED
  build:
    commands:
      - cdk deploy --app "python3 infrastructure/app.py" --all --require-approval never
artifacts:
  files:
    - '**/*'"""


def generate_build_spec_update_branch(
  branch: str,
  account_id: str,
  region: str,
  pull_request_id: str,
  revision_id: str) -> str:
    """Generates the build spec file used for the CodeBuild project"""
    return f"""version: 0.2
env:
  variables:
    BRANCH: {branch}
    ACCOUNT_ID: {account_id}
    REGION: {region}
    PULL_REQUEST_ID: {pull_request_id}
    REVISION_ID: {revision_id}
  parameter-store:
      AWS_CODEBUILD_USER_ACCESS_KEY: CAYLENT_CODEBUILD_USER_ACCESSKEY
      AWS_CODEBUILD_USER_SECRET_KEY: CAYLENT_CODEBUILD_USER_SECRETKEY
phases:
  pre_build:
    commands:
      - apt-get update
      - apt-get install bc -y
      - npm install -g aws-cdk && pip install -r requirements.txt && pip install -r requirements-dev.txt
      - pip install git-remote-codecommit
      - ./infrastructure/scripts/build.sh
      - aws configure set aws_secret_access_key $AWS_CODEBUILD_USER_SECRET_KEY
      - aws configure set aws_access_key_id $AWS_CODEBUILD_USER_ACCESS_KEY
      - aws configure set region $REGION
      - export AWS_ACCOUNT=$ACCOUNT_ID
      - BRANCH_FORMATTED=$(echo "$BRANCH" | sed 's/_//g')
      - BRANCH_FORMATTED=$(echo "$BRANCH_FORMATTED" | sed 's/\///g')
      - export DEPLOYMENT_ENV=$BRANCH_FORMATTED
      - export API_STACK_NAME="$DEPLOYMENT_ENV"-ark-gl-api-stack
      - echo $API_STACK_NAME
  build:
    commands:
      - cd infrastructure/scripts
      - ./check_pylint.sh
      - cd ../..
      - pytest --cov=infrastructure --cov=app tests
      - cd infrastructure/scripts
      - ./check_cdk.sh
      - cd ../..
      - git clone codecommit://wendigo
      - API_URL=$(aws cloudformation describe-stacks --stack-name $API_STACK_NAME | jq '.Stacks | .[] | .Outputs | reduce .[] as $i ({{}}; .[$i.OutputKey] = $i.OutputValue) | .arkglrestapiurl')
      - echo $API_URL
      - export API_URL="$API_URL"v1
      - cd wendigo
      - pip install -r test-requirements.txt
      - make caylent url=$API_URL
      - aws codecommit update-pull-request-approval-state --pull-request-id $PULL_REQUEST_ID --revision-id $REVISION_ID --approval-state APPROVE
artifacts:
  files:
    - '**/*'
    """


def generate_build_spec_destroy_branch(
  branch: str,
  account_id: str,
  region: str,
  artifact_bucket_name: str,
  codebuild_destroy_project: str,
  codebuild_create_project: str) -> str:
    return f"""version: 0.2
env:
  variables:
    BRANCH: {branch}
    ACCOUNT_ID: {account_id}
    REGION: {region}
    CODEBUILD_DESTROY_PROJECT: {codebuild_destroy_project}
    CODEBUILD_CREATE_PROJECT: {codebuild_create_project}
  parameter-store:
    AWS_CODEBUILD_USER_ACCESS_KEY: CAYLENT_CODEBUILD_USER_ACCESSKEY
    AWS_CODEBUILD_USER_SECRET_KEY: CAYLENT_CODEBUILD_USER_SECRETKEY
phases:
  pre_build:
    commands:
      - npm install -g aws-cdk && pip install -r requirements.txt
      - aws configure set aws_secret_access_key $AWS_CODEBUILD_USER_SECRET_KEY
      - aws configure set aws_access_key_id $AWS_CODEBUILD_USER_ACCESS_KEY
      - aws configure set region $REGION
      - export AWS_ACCOUNT=$ACCOUNT_ID
      - BRANCH_FORMATTED=$(echo "$BRANCH" | sed 's/_//g')
      - BRANCH_FORMATTED=$(echo "$BRANCH_FORMATTED" | sed 's/\///g')
      - export DEPLOYMENT_ENV=$BRANCH_FORMATTED
  build:
    commands:
      - cdk destroy --app "python3 infrastructure/app.py" --all --force --require-approval never --method=direct
      - aws s3 rm s3://{artifact_bucket_name}/{branch} --recursive
      - aws codebuild delete-project --name $CODEBUILD_CREATE_PROJECT
      - aws codebuild delete-project --name $CODEBUILD_DESTROY_PROJECT
"""

def generate_build_spec_deploy(
  env: str,
  account_id: str,
  role_arn: str,
  region: str):
    return f"""version: 0.2
env:
  variables:
    ENV: {env}
    ACCOUNT_ID: {account_id}
    REGION: {region}
    ROLE_ARN: {role_arn}
  parameter-store:
    AWS_CODEBUILD_USER_ACCESS_KEY: CAYLENT_CODEBUILD_USER_ACCESSKEY
    AWS_CODEBUILD_USER_SECRET_KEY: CAYLENT_CODEBUILD_USER_SECRETKEY
phases:
  pre_build:
    commands:
      - npm install -g aws-cdk && pip install -r requirements.txt
      - aws configure set aws_secret_access_key $AWS_CODEBUILD_USER_SECRET_KEY
      - aws configure set aws_access_key_id $AWS_CODEBUILD_USER_ACCESS_KEY
      - aws configure set region $REGION
      - export AWS_ACCOUNT=$ACCOUNT_ID
      - export DEPLOYMENT_ENV=$ENV
  build:
    commands:
      - cd infrastructure/scripts
      - chmod 755 deploy.sh
      - chmod 755 deploy_using_role.sh
      - if [ $DEPLOYMENT_ENV = "dev" ]; then ./deploy.sh; else ./deploy_using_role.sh; fi
"""


def get_codebuild_project_name(codebuild_name_prefix, branch, suffix):
    branch_formatted = branch.replace("/", "")
    branch_formatted = branch_formatted.replace(".", "-")
    project_name = f"{codebuild_name_prefix}-{branch_formatted}-{suffix}"
    return project_name
