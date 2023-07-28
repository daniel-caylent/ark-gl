from pyqldb.cursor.buffered_cursor import BufferedCursor
from .qldb_test_base import QldbTestBase

import app.layers.qldb.python.ark_qldb.qldb as qldb

class MockDriver(qldb.Driver):
    def _Driver__execute_single_query(self, query: str, *args) -> list:
        return [query, *args]

class TestQldb(QldbTestBase):

    def test_create_table(self, monkeypatch):
        import app.layers.qldb.python.ark_qldb.qldb as qldb

        test_driver = MockDriver(None, None, None, None, None)

        result = test_driver.create_table("testtable")
        assert None == result

    def test_create_index(self, monkeypatch):
        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.create_index(table_name="testtable", fields=["id"])

        assert None == result

    def test_insert_document(self, monkeypatch):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.insert_document(
            table_name="testtable", document={"id": 1, "name": "test"}
        )

        assert None == result

    def test_read_documents(self, monkeypatch):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.read_documents(
            table_name="testtable", where_clause="1=1"
        )

        assert ["SELECT * FROM testtable WHERE 1=1"] == result

    def test_read_document_fields(self, monkeypatch):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.read_document_fields(
            table_name="testtable", fields=["id", "name"], where_clause="1=1"
        )

        assert ["SELECT id,name FROM testtable WHERE 1=1"] == result

    def test_execute_custom_query(self, monkeypatch):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.execute_custom_query(
            "UPDATE testtable SET name = ? WHERE id = ?", "test2", "1"
        )

        assert ["UPDATE testtable SET name = ? WHERE id = ?", "test2", "1"] == result

    def test_insert_account(self, monkeypatch):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.insert_account(document={"id": 1, "name": "test"})

        assert None == result

    def test_insert_ledger(self, monkeypatch):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.insert_ledger(document={"id": 1, "name": "test"})

        assert None == result

    def test_insert_journal_entry(self, monkeypatch):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.insert_journal_entry(
            document={"id": 1, "name": "test"}
        )

        assert None == result
