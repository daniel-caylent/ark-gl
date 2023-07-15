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

> Note: It is recommended to use lower case values for naming branches and setting up the DEPLOYMENT_ENV

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
AWS_DEFAULT_REGION=aws_region
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

**Before the deployment of the CDK**, we need to build the CDK dependencies.

In the root folder of the repo, consider executing the following script:

```
./infrastructure/scripts/build.sh
```

### CDK:

For provisioning the resources before the deploy (Just execute this a single time per account):
```bash
cdk bootstrap "aws://ACCOUNT_ID/REGION"
```

For creating the infrastructure CloudFormating scripts locally
```bash
cdk synth --app "python3 <app_path>"
```

For deploying the application in the default AWS account
```bash
cdk deploy --app "python3 infrastructure/app.py" --all
```

For deploying the CICD Pipeline
```bash
cdk deploy --app "python3 infrastructure/pipeline_default_app.py" --all
```

For deploying the DR App
```bash
cdk deploy --app "python3 infrastructure/dr_app.py" --all
```

For deploying the QLDB App
```bash
cdk deploy --app "python3 infrastructure/qldb_app.py" --all
```

For deploying the Reconciliation App
```bash
cdk deploy --app "python3 infrastructure/reconciliation_app.py" --all
```

For destroying any application
```bash
cdk destroy --app "python3 <app_path>" --all
```

### Tests execution / Code Coverage

For the tests execution the following command should be executed:
```
pytest tests
```

For gathering code coverage metrics, the following command should be executed:
```
pytest --cov=app tests/
```

### Profiling

Every endpoint is capable of switching into a "profiling mode." To enable profiling, set an environemnt variable PROFILE=1 for any endpoint. When profiling is enabled, the endpoint will process your request as normal, but will not respond with usable data. Profile for the endpoint will be written to the CloudWatch logs. **This is only meant to be used in a development environment.**
