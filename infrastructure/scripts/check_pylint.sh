#! /bin/bash

echo "running pylint..."

(pylint --rcfile ../../.pylintrc ../../app/* --output-format=parseable --reports=y --output pylint_report.log)
PYLINT_EXIT_CODE=$?

# https://pylint.readthedocs.io/en/stable/user_guide/usage/run.html#exit-codes
FATAL_MESSAGE_ISSUED=1
ERROR_MESSAGE_ISSUED=2

cat pylint_report.log

echo "pylint exit code: $PYLINT_EXIT_CODE"

(( FATAL_ERROR = ${PYLINT_EXIT_CODE} & ${FATAL_MESSAGE_ISSUED} ))

if [ $FATAL_ERROR != 0 ]; then
    echo "pylint found a fatal error, please check the report above."
    exit -1
fi

(( ERROR = ${PYLINT_EXIT_CODE} & ${ERROR_MESSAGE_ISSUED} ))

if [ $ERROR != 0 ]; then
    echo "pylint found an error, please check the report above."
    exit -1
fi

echo "pylint has been executed without errors and fatal errors"

echo "checking score threshold..."

MINIMUM_SCORE=8

EXECUTION_SCORE=`cat pylint_report.log | grep -oE "\-?[0-9]+\.[0-9]+" | tail -1`

echo MINIMUM_SCORE=$MINIMUM_SCORE
echo EXECUTION_SCORE=$EXECUTION_SCORE

if [ $(echo "$EXECUTION_SCORE < $MINIMUM_SCORE" | bc -l) -eq 1 ]; then
    echo "Execution score $EXECUTION_SCORE < Minimun Score $MINIMUM_SCORE, exiting with error"
    exit -1;
fi

echo "pylint score is healthy: Execution score $EXECUTION_SCORE, Minimun Score $MINIMUM_SCORE"
