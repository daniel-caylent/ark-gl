import pytest
from mock import Mock

from .ledger_test_base import LedgerTestBase

class TestLedger(LedgerTestBase):
    insert_input = {
        "GLName": "Primary USD based General Ledger",
        "GLDescription": "The details surrounding this specialized General Ledger are beyond the scope of this documentation exercise.",
        "currencyName": "USD",
        "currencyDecimal": 2
    }

    update_input = {
        "GLName": "Primary ARS based General Ledger",
        "GLDescription": "The details General Ledger.",
    }

    max_diff = None

    db = "ARKGL"

    def test_insert(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection

        def get_insert_query(db_, input_, fund_entity_id, region_name, secret_name):
            return (None, None, 'asd-123-456')

        monkeypatch.setattr(ledger, '__get_insert_query', get_insert_query)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = ledger.insert(self.db, self.insert_input, '', '')

        assert 'asd-123-456' == result

    def test_delete(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.fund_entity as fund_entity

        def get_delete_query(db_, id_):
            return (None, None)

        def get_accounts_ledgers_count(db, fund_entity_id, cursor):
            return 1

        monkeypatch.setattr(ledger, '__get_delete_query', get_delete_query)
        monkeypatch.setattr(connection, 'get_connection', Mock())
        monkeypatch.setattr(fund_entity, 'get_accounts_ledgers_count', get_accounts_ledgers_count)

        result = ledger.delete(self.db, 'asd-123-456', '', '')

        assert result is None


    def test_update(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection

        def get_update_query(db_, id_, input_):
            return (None, None)

        monkeypatch.setattr(ledger, '__get_update_query', get_update_query)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = ledger.update(self.db, 'asd-123-456', self.update_input, '', '')

        assert result is None

    def test_get_id(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger

        def select_by_uuid(db, uuid, region_name, secret_name):
            return {'uuid':'abcde', 'id':123, 'name':'ledger'}

        monkeypatch.setattr(ledger, 'select_by_uuid', select_by_uuid)

        result = ledger.get_id(self.db, None, '', '')

        assert 123 == result


    def test_select_by_uuid(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        def execute_single_record_select(conn, params):
            return {'uuid':'abcde', 'id':123, 'name':'ledger'}

        monkeypatch.setattr(connection, 'get_connection', Mock())
        monkeypatch.setattr(db_main, 'execute_single_record_select', execute_single_record_select)

        result = ledger.select_by_uuid(self.db, 'abcde', '', '')

        assert {'uuid':'abcde', 'id':123, 'name':'ledger'} == result
