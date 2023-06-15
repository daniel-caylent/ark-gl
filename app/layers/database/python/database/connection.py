"""This module provides the Aurora MySQL serverless capabilities for the connection methods"""

import json
import pymysql
import boto3

SECRET_DICT = None
CONN = None
READ_CONN = None


def get_connection(
    db_name: str, region_name: str, secret_name: str, db_type: str = None
) -> pymysql.connect:
    """
    This function creates the connection with the db.

    db_name: string
    This parameter specifies the db name where the query will be executed

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    db_type: string (Optional)
    This parameter when set with 'ro' value is used to point the
    read only queries to a specific read only endpoint that will
    be optimized for this type of operations

    return
    A pymysql.connect that represents the actual connection
    """
    global CONN, READ_CONN  # pylint: disable=global-statement; Mechanism needed to reuse the connection

    if db_type == "ro" and READ_CONN is not None:
        READ_CONN.ping(reconnect=True)
        if READ_CONN.open:
            return READ_CONN

    elif db_type != "ro" and CONN is not None:
        CONN.ping(reconnect=True)
        if CONN.open:
            return CONN

    secret_dict = __get_secret(region_name, secret_name)
    host = secret_dict["host"]
    user = secret_dict["username"]
    password = secret_dict["password"]

    if db_type == "ro":
        if secret_dict.get("host-ro") is not None:
            host = secret_dict["host-ro"]
        READ_CONN = pymysql.connect(
            host=host, user=user, password=password, db=db_name, autocommit=True
        )
        return READ_CONN

    CONN = pymysql.connect(host=host, user=user, password=password, db=db_name)

    return CONN


def __get_secret(region_name, secret_name):
    """
    This function retrieves the db credentials' secret from Secrets Manager.

    region_name: string
    This parameter specifies the region where the query will be executed

    secret_name: string
    This parameter specifies the secret manager key name that will contain all
    the information for the connection including the credentials

    return
    A dictionary that contains the credential fields for connecting to the db
    """
    global SECRET_DICT  # pylint: disable=global-statement; Mechanism needed to reuse the secrets

    if SECRET_DICT is not None:
        return SECRET_DICT

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response["SecretString"]

    SECRET_DICT = json.loads(secret)

    return SECRET_DICT
