from . import db_main
from . import connection

def get_all(db:str) -> tuple:
    query = """
        SELECT accatt.id as attributeNo, acctyp.name as accountType, accatt.detail_type as detailType
        FROM """+db+""".account_attribute accatt
        INNER JOIN """+db+""".account_type acctyp ON (accatt.account_type_id = acctyp.id);"""

    return (query, None)

def get_query_select_by_uuid(db:str, uuid:str) -> tuple:
    query = "SELECT * FROM "+db+".account_attribute where uuid = %s;"

    params = (uuid,)

    return (query, params)

def select_by_uuid(db:str, uuid:str, region_name:str, secret_name:str) -> dict:
    params = get_query_select_by_uuid(db, uuid)

    conn = connection.get_connection(db, region_name, secret_name, 'ro')

    record = db_main.execute_single_record_select(conn, params)

    return record

def get_id(db:str, uuid:str, region_name:str, secret_name:str) -> str:
    record = select_by_uuid(db, uuid, region_name, secret_name)

    return record.get('id')
