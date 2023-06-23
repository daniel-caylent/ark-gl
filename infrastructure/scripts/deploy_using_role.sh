#!/bin/bash
set -e

echo "aws sts assume-role: ${ROLE_ARN}"

TEMP_ROLE=$(aws sts assume-role --role-arn $ROLE_ARN --role-session-name ARKGlApi)
export TEMP_ROLE
export AWS_ACCESS_KEY_ID=$(echo "${TEMP_ROLE}" | jq -r '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo "${TEMP_ROLE}" | jq -r '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo "${TEMP_ROLE}" | jq -r '.Credentials.SessionToken')

echo "Role ${role_arn} assumed!"

./deploy.sh