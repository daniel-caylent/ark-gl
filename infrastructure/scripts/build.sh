#! /bin/sh
pip3 install -r ./infrastructure/app/layers/pymysql/requirements.txt -t ./infrastructure/app/layers/pymysql/python
pip3 install -r ./infrastructure/app/layers/pyqldb/requirements.txt -t ./infrastructure/app/layers/pyqldb/python --no-deps
