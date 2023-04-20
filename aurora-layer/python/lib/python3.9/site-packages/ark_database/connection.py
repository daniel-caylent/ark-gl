import pymysql
import boto3
import json


def get_connection(db_name:str, region_name:str, secret_name:str, db_type:str = None) -> pymysql.connect:
    
    secret_dict = json.loads(get_secret(region_name, secret_name))
    host = secret_dict['host']
    user = secret_dict['username']
    password = secret_dict['password'] 

    if db_type == 'ro':
        if secret_dict.get('host-ro') is not None:
            host = secret_dict['host-ro']
    
    conn = pymysql.connect(
        host = host,
        user = user,
        password = password,
        db = db_name
    )
    
    return conn

def get_secret(region_name, secret_name):


    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise 

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return secret