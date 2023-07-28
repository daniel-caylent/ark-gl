from mock import Mock

from .line_item_test_base import LineItemTestBase

class TestLineItem(LineItemTestBase):
    insert_input = {
        "accountId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524ffff",
        "memo": "These charges describe catered Pizza.",
        "entityId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524ffff",
        "amount": 10012
    }

    update_input = {
        "memo": "These charges describe catered Burgers.",
        "amount": 100
    }

    max_diff = None

    db = "ARKGL"


    def test_get_insert_query(self, monkeypatch):
        import app.layers.database.python.database.line_item as line_item
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        def get_id_by_uuid(db, account_uuid, region_name, secret_name):
            return 10

        def get_new_uuid():
            return 'd559fa87-e51a-11ed-aede-0247c1ed2eeb'

        monkeypatch.setattr(account, 'get_id_by_uuid', get_id_by_uuid)
        monkeypatch.setattr(connection, 'get_connection', Mock())
        monkeypatch.setattr(db_main, 'get_new_uuid', get_new_uuid)

        result = line_item.get_insert_query(self.db, self.insert_input, 1, 1, 'Credit', '', '')

        check = "(uuid, account_id, journal_entry_id, line_number, memo, posting_type, amount, entity_id)"

        assert check in result[0]


    def test_get_update_query(self):
        import app.layers.database.python.database.line_item as line_item

        id = "d559fa87-e51a-11ed-aede-0247c1ed2eeb"
        result = line_item.get_update_query(self.db, id, self.update_input)

        update_query = (
        """
        UPDATE """
        + self.db
        + """.line_item
        SET """
        )
        where_clause = " WHERE uuid = %s;"
        set_clause = """memo = %s,
amount = %s
"""

        wanted_result = (
            update_query+set_clause+where_clause,
            (
                self.update_input["memo"], self.update_input["amount"], id
            )
        )

        assert wanted_result == result


    def test_get_delete_query(self):
        import app.layers.database.python.database.line_item as line_item

        id = "d559fa87-e51a-11ed-aede-0247c1ed2eeb"
        result = line_item.get_delete_query(self.db, id)

        query = (
        """
        DELETE FROM """
        + self.db
        + """.line_item
        WHERE uuid = %s;"""
        )

        wanted_result = (
            query,
            (
                id,
            )
        )

        assert wanted_result == result


    def test_get_delete_by_journal_query(self):
        import app.layers.database.python.database.line_item as line_item

        journal_id = "journal-123"
        result = line_item.get_delete_by_journal_query(self.db, journal_id)

        query = (
        """
        DELETE FROM """
        + self.db
        + """.line_item
        WHERE journal_entry_id = %s;"""
        )

        wanted_result = (
            query,
            (
                journal_id,
            )
        )

        assert wanted_result == result


    def test_select_by_number_journal(self, monkeypatch):
        import app.layers.database.python.database.line_item as line_item
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        def execute_single_record_select(conn, params):
            return {'uuid':'abcde', 'line_number': 1, 'journal_id': 1, 'memo':'line'}

        monkeypatch.setattr(connection, 'get_connection', Mock())
        monkeypatch.setattr(db_main, 'execute_single_record_select', execute_single_record_select)

        result = line_item.select_by_number_journal(self.db, 1, 1, '', '')

        assert {'uuid':'abcde', 'line_number': 1, 'journal_id': 1, 'memo':'line'} == result


    def test_select_numbers_by_journal(self, monkeypatch):
        import app.layers.database.python.database.line_item as line_item
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        def execute_multiple_record_select(conn, params):
            return [{'uuid':'abcde', 'line_number': 1}, {'uuid':'fghijk', 'line_number': 2}]

        monkeypatch.setattr(connection, 'get_connection', Mock())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', execute_multiple_record_select)

        result = line_item.select_numbers_by_journal(self.db, 1, '', '')

        assert [{'uuid':'abcde', 'line_number': 1}, {'uuid':'fghijk', 'line_number': 2}] == result