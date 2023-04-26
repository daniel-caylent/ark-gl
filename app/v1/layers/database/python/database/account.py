from . import db_main
from . import connection
from . import account_attribute
from . import fund_entity

app_to_db = {
    'accountId': 'uuid',
    'fundId': 'fund_entity_id',
    'accountNo': 'account_no',
    'state': 'state',
    'parentAccountNo': 'parent_id',
    'accountName': 'name',
    'accountDescription': 'description',
    'attributeId': 'account_attribute_id',
    'isHidden': 'is_hidden',
    'isTaxable': 'is_taxable',
    'isVendorCustomerPartnerRequired': 'is_vendor_customer_partner_required',
    'fsMappingId': 'fs_mapping_id',
    'fsName': 'fs_name',
    'isDryRun': 'is_dry_run'
}

def get_query_insert(db:str, input:dict, region_name:str, secret_name:str) -> tuple:
    query = """
        INSERT INTO """+db+""".account
            (uuid, account_no, fund_entity_id, account_attribute_id, parent_id, name, description,
            state, is_hidden, is_taxable, is_vendor_customer_partner_required)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s);"""
    
    translated_input = db_main.translate_to_db(app_to_db, input)

    fund_entity_uuid = translated_input.get('fund_entity_id')
    fund_entity_id = fund_entity.get_id(db, fund_entity_uuid, region_name, secret_name)
    account_attribute_uuid = translated_input.get('account_attribute_id')
    account_attribute_id = account_attribute.get_id(db, account_attribute_uuid, region_name, secret_name)

    # Getting new uuid from the db to return it in insertion
    ro_conn = connection.get_connection(db, region_name, secret_name, 'ro')
    uuid = db_main.get_new_uuid(ro_conn)

    params = (
        uuid,
        translated_input.get('account_no'),
        fund_entity_id,
        account_attribute_id,
        translated_input.get('parent_id'),
        translated_input.get('name'),
        translated_input.get('description'),
        translated_input.get('state'),
        translated_input.get('is_hidden'),
        translated_input.get('is_taxable'),
        translated_input.get('is_vendor_customer_partner_required')
    )

    return (query, params, uuid)

def get_query_update(db:str, id:str, input:dict) -> tuple:
    update_query = """
        UPDATE """+db+""".account
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

def get_query_delete(db:str, id:str) -> tuple:
    query = """
        DELETE FROM """+db+""".account
        WHERE uuid = %s;"""
    
    params = (id,)

    return (query, params)

def get_query_select_by_uuid(db:str, uuid:str) -> tuple:
    query = "SELECT * FROM "+db+".account where uuid = %s;"

    params = (uuid,)

    return (query, params)

def get_query_select_by_fund(db:str, fund_id:str) -> tuple:
    query = """
        SELECT acc.*
        FROM """+db+""".account acc
        INNER JOIN """+db+""".fund_entity fe ON (acc.fund_entity_id = fe.id)
        where fe.uuid = %s;"""

    params = (fund_id,)

    return (query, params)

def get_query_select_by_name(db:str, account_name:str) -> tuple:
    account_name = account_name.lower().strip()
    query = """
        SELECT *
        FROM """+db+""".account
        where TRIM(LOWER(name)) = %s;"""

    params = (account_name,)

    return (query, params)

def insert(db:str, input:dict, region_name:str, secret_name:str) -> str:
    params = get_query_insert(db, input, region_name, secret_name)

    query_params = [params[0], params[1]]
    uuid = params[2]

    conn = connection.get_connection(db, region_name, secret_name)

    query_list = [query_params]

    db_main.execute_dml(conn, query_list)

    return uuid
