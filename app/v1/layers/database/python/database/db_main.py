from pymysql import Connection, cursors

def translate_to_db(app_to_db:dict, input:dict) -> dict:
    return dict((app_to_db[key], value) for (key, value) in input.items())

def translate_to_app(app_to_db: dict, input:dict) -> dict:
    results = None
    if input is not None:
        db_to_app = {v: k for k, v in app_to_db.items()}
        results = dict((db_to_app.get(key,f'missing-{key}'), value) for (key, value) in input.items())
    return results

def execute_dml(connection:Connection, query_list:list[tuple]) -> None:
    cursor = connection.cursor()

    try:
        for item in query_list:
            query = item[0]
            data = item[1]
            cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()
    
    return

def execute_single_record_select(connection:Connection, query_params:tuple) -> dict:
    cursor = connection.cursor(cursors.DictCursor)

    try:
        query = query_params[0]
        data = query_params[1]
        cursor.execute(query, data)
        record = cursor.fetchone()
    except Exception as e:
        raise
    finally:
        cursor.close()
        connection.close()
    
    return record

def execute_multiple_record_select(connection:Connection, query_params:tuple) -> list[dict]:
    cursor = connection.cursor(cursors.DictCursor)

    try:
        query = query_params[0]
        data = query_params[1]
        cursor.execute(query, data)
        record_list = cursor.fetchall()
    except Exception as e:
        raise
    finally:
        cursor.close()
        connection.close()
    
    return record_list

def get_new_uuid(connection:Connection) -> str:
    params = ("SELECT UUID() as id;", None)

    # conn = connection.get_connection(db, region_name, secret_name, 'ro')

    record = execute_single_record_select(connection, params)

    return record.get('id')
