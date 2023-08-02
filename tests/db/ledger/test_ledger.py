
from tests.mock.db import MockConn, MockCursor

from .ledger_test_base import LedgerTestBase


MOCK_RECORD = {
    "fund_entity_id": "fundid",
    "client_id": "clientid",
    "uuid": "uuid",
    "name": "",
    "description": "",
    "state": "",
    "currency": "",
    "decimals": "",
    "post_date": "",
}

MOCK_INPUT = {
        "glName": "Primary USD based General Ledger",
        "glDescription": "The details surrounding this specialized General Ledger are beyond the scope of this documentation exercise.",
        "currencyName": "USD",
        "currencyDecimal": 2
    }


class TestLedger(LedgerTestBase):

    update_input = {
        "GLName": "Primary ARS based General Ledger",
        "GLDescription": "The details General Ledger.",
    }

    max_diff = None

    db = "ARKGL"



    def test_insert(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main


        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'get_new_uuid', lambda *args: "GENERATED UUID")

        result = ledger.insert("db", MOCK_INPUT, '', '')

        assert "GENERATED UUID" == result


    def test_select_committed_between_dates(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_RECORD])

        ledger.select_committed_between_dates("db", "startDate", "endDate", '', '')

    def test_delete(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_RECORD])

        ledger.delete("db", "id", '', '')

    def test_update(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_RECORD])

        ledger.update("db", "id", {"glName": "TEST"}, '', '')

    def test_select_by_uuid(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_RECORD)

        ledger.select_by_uuid("db", "id", '', '')

    def test_select_by_fund(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_RECORD])

        ledger.select_by_fund("db", "fundid", '', '')

    def test_select_by_name(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_RECORD])

        ledger.select_by_name("db", "name", '', '')

    def test_select_by_client_id(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_RECORD])

        ledger.select_by_client_id("db", "clientId", '', '')

    def test_get_id(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_RECORD)

        ledger.get_id("db", "id", '', '')

    def test_select_count_with_post_date(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: {
            "count(*)": 1
        })

        ledger.select_count_with_post_date("db",'', '')

    def test_select_by_multiple_uuids(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_RECORD])

        ledger.select_by_multiple_uuids("db", "clientId", '', '')
    
    def test_select_by_fund_and_name(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: MOCK_RECORD)

        ledger.select_by_fund_and_name("db", "fund", "name", '', '')

    def test_select_by_uuid_with_cursor(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_RECORD)

        ledger.select_by_uuid_with_cursor("db", "id", MockCursor())

    def test_bulk_delete(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_RECORD])
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_RECORD)

        ledger.bulk_delete("db", "id", '', '')


    def test_bulk_state(self, monkeypatch):
        import app.layers.database.python.database.ledger as ledger
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())

        ledger.bulk_state("db", ["id"], '', '')



    # def test_delete(self, monkeypatch):
    #     import app.layers.database.python.database.ledger as ledger
    #     import app.layers.database.python.database.connection as connection
    #     import app.layers.database.python.database.fund_entity as fund_entity

    #     def get_delete_query(db_, id_):
    #         return (None, None)

    #     def get_accounts_ledgers_count(db, fund_entity_id, cursor):
    #         return 1

    #     monkeypatch.setattr(ledger, '__get_delete_query', get_delete_query)
    #     monkeypatch.setattr(connection, 'get_connection', Mock())
    #     monkeypatch.setattr(fund_entity, 'get_accounts_ledgers_count', get_accounts_ledgers_count)

    #     result = ledger.delete(self.db, 'asd-123-456', '', '')

    #     assert result is None


    # def test_update(self, monkeypatch):
    #     import app.layers.database.python.database.ledger as ledger
    #     import app.layers.database.python.database.connection as connection

    #     def get_update_query(db_, id_, input_):
    #         return (None, None)

    #     monkeypatch.setattr(ledger, '__get_update_query', get_update_query)
    #     monkeypatch.setattr(connection, 'get_connection', Mock())

    #     result = ledger.update(self.db, 'asd-123-456', self.update_input, '', '')

    #     assert result is None

    # def test_get_id(self, monkeypatch):
    #     import app.layers.database.python.database.ledger as ledger

    #     def select_by_uuid(db, uuid, region_name, secret_name):
    #         return {'uuid':'abcde', 'id':123, 'name':'ledger'}

    #     monkeypatch.setattr(ledger, 'select_by_uuid', select_by_uuid)

    #     result = ledger.get_id(self.db, None, '', '')

    #     assert 123 == result


    # def test_select_by_uuid(self, monkeypatch):
    #     import app.layers.database.python.database.ledger as ledger
    #     import app.layers.database.python.database.connection as connection
    #     import app.layers.database.python.database.db_main as db_main

    #     def execute_single_record_select(conn, params):
    #         return {'uuid':'abcde', 'id':123, 'name':'ledger'}

    #     monkeypatch.setattr(connection, 'get_connection', Mock())
    #     monkeypatch.setattr(db_main, 'execute_single_record_select', execute_single_record_select)

    #     result = ledger.select_by_uuid(self.db, 'abcde', '', '')

    #     assert {'uuid':'abcde', 'id':123, 'name':'ledger'} == result
