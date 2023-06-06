#! /bin/sh
set -e

cdk synth --app "python3 ../app.py"
cdk synth --app "python3 ../dr_app.py"
cdk synth --app "python3 ../reconciliation_app.py"
cdk synth --app "python3 ../pipeline_default_app.py"
cdk synth --app "python3 ../qldb_app.py"