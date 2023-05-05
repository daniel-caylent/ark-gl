#! /bin/sh
pip3 install -r ./infrastructure/app/layers/pymysql/requirements.txt -t ./infrastructure/app/layers/pymysql/python
pip3 install -r ./infrastructure/app/layers/qldb_requirements/requirements.txt -t ./infrastructure/app/layers/qldb_requirements/python --no-deps
