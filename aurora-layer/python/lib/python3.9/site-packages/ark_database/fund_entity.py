import db_main
import connection

# app_to_db = {
#     'fundId': 'uuid',
#     'clientId': 'client_id',
#     # '': 'fund_id'
# }

def get_query_select_by_uuid(db:str, uuid:str) -> tuple:
    query = "SELECT * FROM "+db+".fund_entity where uuid = %s;"

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
