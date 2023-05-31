from mock import Mock

from .attachment_test_base import AttachmentTestBase


class TestAttachment(AttachmentTestBase):
    insert_input = {
        "documentId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
        "documentMemo": "Scanned Receipt for Office Pizza Party.",
    }

    update_input = {"documentMemo": "Scanned Receipt for Office Burgers Party."}

    db = "ARKGL"

    def test_get_insert_query(self, monkeypatch):
        import app.v1.layers.database.python.database.attachment as attachment

        result = attachment.get_insert_query(self.db, self.insert_input, 1)

        wanted_result = (
            """
        INSERT INTO """
            + self.db
            + """.attachment
            (uuid, journal_entry_id, memo)
        VALUES
            (%s, %s, %s);""",
            (
                "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
                1,
                "Scanned Receipt for Office Pizza Party.",
            ),
        )

        assert wanted_result == result

    def test_get_update_query(self):
        import app.v1.layers.database.python.database.attachment as attachment

        id = "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123"
        result = attachment.get_update_query(self.db, id, self.update_input)

        update_query = (
            """
        UPDATE """
            + self.db
            + """.attachment
        SET """
        )
        where_clause = " WHERE uuid = %s;"
        set_clause = """memo = %s
"""

        wanted_result = (
            update_query + set_clause + where_clause,
            (self.update_input["documentMemo"], id),
        )

        assert wanted_result == result

    def test_get_delete_query(self):
        import app.v1.layers.database.python.database.attachment as attachment

        id = "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123"
        result = attachment.get_delete_query(self.db, id)

        query = (
            """
        DELETE FROM """
            + self.db
            + """.attachment
        WHERE uuid = %s;"""
        )

        wanted_result = (query, (id,))

        assert wanted_result == result

    def test_get_delete_by_journal_query(self):
        import app.v1.layers.database.python.database.attachment as attachment

        journal_id = "1"
        result = attachment.get_delete_by_journal_query(self.db, journal_id)

        query = (
            """
        DELETE FROM """
            + self.db
            + """.attachment
        WHERE journal_entry_id = %s;"""
        )

        wanted_result = (query, (journal_id,))

        assert wanted_result == result

    def test_select_by_document_id(self, monkeypatch):
        import app.v1.layers.database.python.database.attachment as attachment
        import app.v1.layers.database.python.database.connection as connection
        import app.v1.layers.database.python.database.db_main as db_main

        def execute_single_record_select(conn, params):
            return {
                "uuid": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
                "journal_id": 1,
                "memo": "Scanned Receipt for Office Pizza Party.",
            }

        monkeypatch.setattr(connection, "get_connection", Mock())
        monkeypatch.setattr(
            db_main, "execute_single_record_select", execute_single_record_select
        )

        result = attachment.select_by_document_id(
            self.db, "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123", "", ""
        )

        assert {
            "uuid": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
            "journal_id": 1,
            "memo": "Scanned Receipt for Office Pizza Party.",
        } == result

    def test_select_by_journal(self, monkeypatch):
        import app.v1.layers.database.python.database.attachment as attachment
        import app.v1.layers.database.python.database.connection as connection
        import app.v1.layers.database.python.database.db_main as db_main

        def execute_multiple_record_select(conn, params):
            return [
                {
                    "uuid": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
                    "journal_id": 2,
                    "memo": "Scanned Receipt for Office Pizza Party.",
                },
                {
                    "uuid": "ab84c7c6-9f62-11ed-8cf5-0ed8d524e124",
                    "journal_id": 2,
                    "memo": "Scanned Receipt for Office Coke Party.",
                },
            ]

        monkeypatch.setattr(connection, "get_connection", Mock())
        monkeypatch.setattr(
            db_main, "execute_multiple_record_select", execute_multiple_record_select
        )

        result = attachment.select_by_journal(self.db, 2, "", "")

        assert [
            {
                "uuid": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
                "journal_id": 2,
                "memo": "Scanned Receipt for Office Pizza Party.",
            },
            {
                "uuid": "ab84c7c6-9f62-11ed-8cf5-0ed8d524e124",
                "journal_id": 2,
                "memo": "Scanned Receipt for Office Coke Party.",
            },
        ] == result

    def test_select_by_multiple_journals(self, monkeypatch):
        import app.v1.layers.database.python.database.attachment as attachment
        import app.v1.layers.database.python.database.connection as connection
        import app.v1.layers.database.python.database.db_main as db_main

        def execute_multiple_record_select(conn, params):
            return [
                {
                    "uuid": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
                    "journal_id": 2,
                    "memo": "Scanned Receipt for Office Pizza Party.",
                },
                {
                    "uuid": "ab84c7c6-9f62-11ed-8cf5-0ed8d524e124",
                    "journal_id": 3,
                    "memo": "Scanned Receipt for Office Coke Party.",
                },
            ]

        monkeypatch.setattr(connection, "get_connection", Mock())
        monkeypatch.setattr(
            db_main, "execute_multiple_record_select", execute_multiple_record_select
        )

        result = attachment.select_by_multiple_journals(self.db, [2, 3], "", "")

        assert [
            {
                "uuid": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
                "journal_id": 2,
                "memo": "Scanned Receipt for Office Pizza Party.",
            },
            {
                "uuid": "ab84c7c6-9f62-11ed-8cf5-0ed8d524e124",
                "journal_id": 3,
                "memo": "Scanned Receipt for Office Coke Party.",
            },
        ] == result
