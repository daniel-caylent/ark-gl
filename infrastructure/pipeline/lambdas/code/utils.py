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
  build:
    commands:
        - pytest --cov=infrastructure --cov=app tests
        - aws configure set aws_secret_access_key $AWS_CODEBUILD_USER_SECRET_KEY
        - aws configure set aws_access_key_id $AWS_CODEBUILD_USER_ACCESS_KEY
        - cd infrastructure/scripts
        - ./check_pylint.sh
        - ./check_cdk.sh
        - BRANCH_FORMATTED=$(echo "$BRANCH" | sed 's/_//g')
        - BRANCH_FORMATTED=$(echo "$BRANCH_FORMATTED" | sed 's/\///g')
        - export DEPLOYMENT_ENV=$BRANCH_FORMATTED
        - cd ../..
        - cdk deploy --app "python3 infrastructure/app.py" --all --require-approval never
artifacts:
  files:
    - '**/*'"""

def generate_build_spec_destroy_branch(branch: str, account_id: str, region: str) -> str:
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
        """  # TODO: to be done



def get_codebuild_project_name(codebuild_name_prefix, branch, suffix):
    branch_formatted = branch.replace("/", "")
    project_name = f"{codebuild_name_prefix}-{branch_formatted}-{suffix}"
    return project_name


def destroy_branch_resources(client):
    client.delete_project(name=project_name)

    client.create_project(
        name=f'{codebuild_name_prefix}-{branch}-destroy',
        description="Build project to destroy branch resources",
        source={
            'type': 'S3',
            'location': f'{artifact_bucket_name}/{branch}/CodeBuild-{branch}-create/',
            'buildspec': generate_build_spec_create_branch(branch)
        },
        artifacts={
            'type': 'NO_ARTIFACTS'
        },
        environment={
            'type': 'LINUX_CONTAINER',
            'image': 'aws/codebuild/standard:6.0',
            'computeType': 'BUILD_GENERAL1_SMALL'
        },
        serviceRole=role_arn
    )

    client.start_build(
        projectName=f'CodeBuild-{branch}-destroy'
    )

    client.delete_project(
        name=f'CodeBuild-{branch}-destroy'
    )

    client.delete_project(
        name=f'CodeBuild-{branch}-create'
    )


