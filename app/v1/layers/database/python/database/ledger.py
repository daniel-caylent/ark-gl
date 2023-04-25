import db_main
import connection

app_to_db = {
    'ledgerId': 'uuid',
    'GLName': 'name',
    'GLDescription': 'description',
    'currencyName': 'currency',
    'currencyDecimal': 'decimal',
    'isHidden': 'is_hidden'
}

def get_insert_query(db:str, input:dict) -> tuple:
    query = """
        INSERT INTO """+db+""".ledger
            (uuid, fund_entity_id, name, description, state, is_hidden, currency,  `decimal`)
        VALUES
            (%s, %s, %s, %s, %s, %s,
            %s, %s);"""
    
    translated_input = db_main.translate_to_db(app_to_db, input)

    params = (
        translated_input.get('uuid'),
        translated_input.get('fund_entity_id'),
        translated_input.get('name'),
        translated_input.get('description'),
        translated_input.get('state'),
        translated_input.get('is_hidden'),
        translated_input.get('currency'),
        translated_input.get('decimal')
    )

    return (query, params)

def get_update_query(db:str, id:str, input:dict) -> tuple:
    
    update_query = """
        UPDATE """+db+""".ledger
        SET """
    where_clause = "WHERE uuid = %s;"
    
    translated_input = db_main.translate_to_db(app_to_db, input)

    set_clause = ''
    params = ()
    for key in translated_input.keys():
        set_clause += str(key)+" = %s\n"
        params += (translated_input.get(key),)
    
    params += (id,)

    query = update_query+set_clause+where_clause

    return (query, params)

def get_delete_query(db:str, id:str) -> tuple:
    query = """
        DELETE FROM """+db+""".ledger
        WHERE uuid = %s;"""
    
    params = (id,)

    return (query, params)

def get_by_id(db:str, id:str) -> tuple:
    query = "SELECT * FROM "+db+".ledger where uuid = %s;"

    params = (id,)

    return (query, params)

def get_by_fund(db:str, fund_id:str) -> tuple:
    query = """
        SELECT le.*
        FROM """+db+""".ledger le
        INNER JOIN """+db+""".fund_entity fe ON (le.fund_entity_id = fe.id)
        where fe.uuid = %s;"""

    params = (fund_id,)

    return (query, params)

def get_by_name(db:str, account_name:str) -> tuple:
    account_name = account_name.lower().strip()
    query = """
        SELECT *
        FROM """+db+""".ledger
        where TRIM(LOWER(name)) = %s;"""

    params = (account_name,)

    return (query, params)

def insert(db:str, input:dict, region_name:str, secret_name:str, db_type:str = None) -> None:
    params = get_insert_query(db, input, region_name, secret_name)

    conn = connection.get_connection(db, region_name, secret_name, db_type)

    query_list = [params]

    db_main.execute_dml(conn, query_list)

    return