# ark-ledger

Code + Infrastructure repository for the Ark-Legder project, created by Caylent.

## Description

This CDK-based project will provision the entire architecture for the Arl-Ledger black box.

The business application is located in the `app` folder.

The infrastructure is located in the `infrastructure` folder.

## Instructions

### Personal environments:

To have your own provisioned architecture (represented as a prefix in the CloudFormation stack name), consider setting up the following environment variable:

```bash
DEPLOYMENT_ENV=my-account-name
```

### Building up the layer's dependencies

Before the deployment of the CDK, we need to build the CDK dependencies.

In the root folder of the repo, consider executing the following script:

```
./infrastructure/scripts/build.sh
```

### CDK:

For provisioning the resources before the deploy:
```bash
cdk boostrap
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
