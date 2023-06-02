#! /bin/sh
pip3 install -r ./infrastructure/shared/layers/pymysql/requirements.txt -t ./infrastructure/shared/layers/pymysql/python
pip3 install -r ./infrastructure/shared/layers/pyqldb/requirements.txt -t ./infrastructure/shared/layers/pyqldb/python --no-deps
