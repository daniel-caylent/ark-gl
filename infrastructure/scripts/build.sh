#! /bin/sh
pip install -r ./infrastructure/shared/layers/pymysql/requirements.txt
pip install -r ./infrastructure/shared/layers/pyqldb/requirements.txt --no-deps

pip install -r ./infrastructure/shared/layers/pymysql/requirements.txt -t ./infrastructure/shared/layers/pymysql/python
pip install -r ./infrastructure/shared/layers/pyqldb/requirements.txt -t ./infrastructure/shared/layers/pyqldb/python --no-deps
