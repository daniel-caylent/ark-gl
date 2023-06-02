# ark-ledger

Code + Infrastructure repository for the Ark-Legder project, created by Caylent.

## Description

This CDK-based project will provision the entire architecture for the Arl-Ledger black box.

The business application is located in the `app` folder.

The infrastructure is located in the `infrastructure` folder.

## Instructions

### Requirements

- python 3.10+

- aws_cdk 2.74.0+

#### Setup environment variables

To have your own provisioned architecture (represented as a prefix in the CloudFormation stack name), consider setting up the following environment variable:

```bash
DEPLOYMENT_ENV=environment
```

This variable dictates what VPC, Subnets and Secrets should be used per environment.
All the configurations resides in the file `infrastructure/app/env.py`.

Note:

    - If the `DEPLOYMENT_ENV=prod`, the cdk will be deployed using the production resource ids

    - If the `DEPLOYMENT_ENV=qa`, the cdk will be deployed using the qa resource ids

    - If any other value is set up for the `DEPLOYMENT_ENV`, the cdk will be deployed using the dev resource ids


There are other environments that should be set up
```bash
AWS_ACCOUNT=aws_account_id
AWS_REGION=aws_region
```

#### Creating a virtual environment

Make sure your python version is 3.10+

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

python --version
```

### Building up the layer's dependencies

Before the deployment of the CDK, we need to build the CDK dependencies.

In the root folder of the repo, consider executing the following script:

```
./infrastructure/scripts/build.sh
```

### CDK:

For provisioning the resources before the deploy (Just execute this a single time per account):
```bash
cdk bootstrap
```

For creating the infrastructure CloudFormating scripts locally
```bash
cdk synth
```

For deploying the application in the default AWS account
```bash
cdk deploy --all

cdk deploy <stack_name>
```

For deploying the pipeline
```bash
cdk deploy --app "python3 pipeline_app.py"
```

### Tests execution / Code Coverage

For the tests execution the following command should be executed:
```
pytest tests
```

For gathering code coverage metrics, the following commands should be executed:
```
pytest --cov=app tests

pytest --cov=infrastructure tests
```
