"""This module provides the Aurora MySQL serverless capabilities for the connection methods"""
import pymysql
import boto3
import json

secret_dict = None
conn = None
read_conn = None


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
    global conn, read_conn

    if db_type == "ro" and read_conn is not None:
        read_conn.ping(reconnect=True)
        if read_conn.open:
            return read_conn

    elif db_type != "ro" and conn is not None:
        conn.ping(reconnect=True)
        if conn.open:
            return conn

    secret_dict = __get_secret(region_name, secret_name)
    host = secret_dict["host"]
    user = secret_dict["username"]
    password = secret_dict["password"]

    if db_type == "ro":
        if secret_dict.get("host-ro") is not None:
            host = secret_dict["host-ro"]
        read_conn = pymysql.connect(host=host, user=user, password=password, db=db_name, autocommit=True)
        return read_conn

    conn = pymysql.connect(host=host, user=user, password=password, db=db_name)

    return conn


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
    global secret_dict

    if secret_dict is not None:
        return secret_dict

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response["SecretString"]

    secret_dict = json.loads(secret)

    return secret_dict
