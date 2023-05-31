import pytest
from mock import Mock

from .accounts_test_base import AccountsTestBase

class TestAccount(AccountsTestBase):

    insert_input = {
        "accountNo": 778897,
        "fundId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
        "parentAccountNo": 1234567,
        "accountName": "Miscellaneous Expenses.",
        "accountDescription": "Miscellaneous Expenses is an aggregation account that includes all miscellaneous expenses including pizza and burritos.",
        "attributeNo": 2,
        "FSMappingId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
        "FSName": "FSMapping is used for reporting purposes.",
        "isTaxable": True,
        "isEntityRequired": False,
        "isDryRun": False
    }

    update_input = {
        "accountName": "Miscellaneous Expenses UPDATED 123",
        "FSName": "UPDATED: FSMapping is used for reporting purposes."
    }

    max_diff = None

    db = "ARKGL"

    
    def test_insert(self, monkeypatch):
        import app.v1.layers.database.python.database.account as account
        import app.v1.layers.database.python.database.connection as connection

        def get_insert_query(db, input, region_name, secret_name):
            return (None, None, 'asd-123-456',
                    {
                        "fs_mapping_id": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
                        "fs_name": "FSMapping is used for reporting purposes."
                    }
            )

        monkeypatch.setattr(account, '__get_insert_query', get_insert_query)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = account.insert(self.db, self.insert_input, '', '')

        assert 'asd-123-456' == result


    def test_delete(self, monkeypatch):

        import app.v1.layers.database.python.database.account as account
        import app.v1.layers.database.python.database.connection as connection

        def get_delete_query(db, id):
            return (None, None)

        monkeypatch.setattr(account, '__get_delete_query', get_delete_query)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = account.delete(self.db, 'asd-123-456', '', '')

        assert None == result


    def test_update(self, monkeypatch):

        import app.v1.layers.database.python.database.account as account
        import app.v1.layers.database.python.database.connection as connection

        def get_update_query(db, id, input, region_name, secret_name):
            return (None, None)

        monkeypatch.setattr(account, '__get_update_query', get_update_query)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = account.update(self.db, 'asd-123-456', self.update_input, '', '')

        assert None == result


    def test_select_by_number(self, monkeypatch):
        import app.v1.layers.database.python.database.account as account
        import app.v1.layers.database.python.database.connection as connection
        import app.v1.layers.database.python.database.db_main as db_main

        def execute_single_record_select(conn, params):
            return {'uuid':'abcde', 'id':123, 'name':'account'}

        monkeypatch.setattr(db_main, 'execute_single_record_select', execute_single_record_select)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = account.select_by_number(self.db, None, '', '')

        assert {'uuid':'abcde', 'id':123, 'name':'account'} == result


    def test_get_id(self, monkeypatch):
        import app.v1.layers.database.python.database.account as account

        def select_by_number(db, account_number, region_name, secret_name):
            return {'uuid':'abcde', 'id':123, 'name':'account'}

        monkeypatch.setattr(account, 'select_by_number', select_by_number)

        result = account.get_id_by_number(self.db, None, '', '')

        assert 123 == result


    def test_select_by_uuid(self, monkeypatch):
        import app.v1.layers.database.python.database.account as account
        import app.v1.layers.database.python.database.connection as connection
        import app.v1.layers.database.python.database.db_main as db_main

        def execute_single_record_select(conn, params):
            return {'uuid':'abcde', 'id':123, 'name':'account'}

        monkeypatch.setattr(db_main, 'execute_single_record_select', execute_single_record_select)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = account.select_by_uuid(self.db, 'abcde', '', '')

        assert {'uuid':'abcde', 'id':123, 'name':'account'} == result


    def test_select_by_fund(self, monkeypatch):
        import app.v1.layers.database.python.database.account as account
        import app.v1.layers.database.python.database.connection as connection
        import app.v1.layers.database.python.database.db_main as db_main

        def execute_multiple_record_select(conn, params):
            return [{'uuid':'abcde', 'id':123, 'name':'account'}]

        monkeypatch.setattr(db_main, 'execute_multiple_record_select', execute_multiple_record_select)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = account.select_by_fund(self.db, 'abcde', '', '')

        assert [{'uuid':'abcde', 'id':123, 'name':'account'}] == result


    def test_select_by_name(self, monkeypatch):
        import app.v1.layers.database.python.database.account as account
        import app.v1.layers.database.python.database.connection as connection
        import app.v1.layers.database.python.database.db_main as db_main

        def execute_single_record_select(conn, params):
            return {'uuid':'abcde', 'id':123, 'name':'account'}

        monkeypatch.setattr(db_main, 'execute_single_record_select', execute_single_record_select)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = account.select_by_name(self.db, 'abcde', '', '')

        assert {'uuid':'abcde', 'id':123, 'name':'account'} == result
