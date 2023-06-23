#!/bin/bash
set -e

cdk bootstrap "aws://${ACCOUNT_ID}/${REGION}"

cd ../..

./infrastructure/scripts/build.sh

cdk deploy --app "python3 infrastructure/app.py" --method=direct --all --require-approval never