#! /bin/sh
set -e
export AWS_ACCOUNT=319244063014
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=dummy_access_key
export AWS_SECRET_ACCESS_KEY=dummy_secret_key
cdk synth --app "python3 ../app.py"
cdk synth --app "python3 ../dr_app.py"
cdk synth --app "python3 ../reconciliation_app.py"
cdk synth --app "python3 ../pipeline_default_app.py"
cdk synth --app "python3 ../qldb_app.py"