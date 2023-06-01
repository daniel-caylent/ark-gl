from mock import Mock

from .fs_test_base import FsTestBase


class TestFs(FsTestBase):
    insert_input = {
        "fs_mapping_id": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
        "fs_name": "fsnametest123",
    }

    update_input = {"fs_name": "fsnametest456"}

    db = "ARKGL"

    def test_get_insert_query(self, monkeypatch):
        import app.layers.database.python.database.fs as fs

        result = fs.get_insert_query(self.db, self.insert_input)

        wanted_result = (
            """
        INSERT INTO """
            + self.db
            + """.FS
            (fs_mapping_id, fs_name)
        VALUES
            (%s, %s);""",
            (
                "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
                "fsnametest123",
            ),
        )

        assert wanted_result == result

    def test_get_update_query(self):
        import app.layers.database.python.database.fs as fs

        id = "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123"
        result = fs.get_update_query(self.db, id, self.update_input)

        update_query = (
            """
        UPDATE """
            + self.db
            + """.FS
        SET """
        )
        where_clause = " WHERE fs_mapping_id = %s;"
        set_clause = """fs_name = %s
"""

        wanted_result = (
            update_query + set_clause + where_clause,
            (self.update_input["fs_name"], id),
        )

        assert wanted_result == result

    def test_get_delete_query(self):
        import app.layers.database.python.database.fs as fs

        id = "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123"
        result = fs.get_delete_query(self.db, id)

        query = (
            """
        DELETE FROM """
            + self.db
            + """.FS
        WHERE fs_mapping_id = %s;"""
        )

        wanted_result = (query, (id,))

        assert wanted_result == result

    def test_select_by_fs_mapping_id(self, monkeypatch):
        import app.layers.database.python.database.fs as fs
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        def execute_single_record_select(conn, params):
            return {
                "fs_mapping_id": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
                "fs_name": "fsnametest456",
            }

        monkeypatch.setattr(connection, "get_connection", Mock())
        monkeypatch.setattr(
            db_main, "execute_single_record_select", execute_single_record_select
        )

        result = fs.select_by_fs_mapping_id(
            self.db, "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123", "", ""
        )

        assert {
            "fs_mapping_id": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
            "fs_name": "fsnametest456",
        } == result
