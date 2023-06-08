#! /bin/sh
set -e

pytest tests

cd infrastructure/scripts
./synth_apps.sh