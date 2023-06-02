from .qldb_test_base import QldbTestBase


class TestQldb(QldbTestBase):
    import app.layers.qldb.python.ark_qldb.qldb as qldb

    test_driver = qldb.Driver(None, None, None, None, None)

    def execute_query(self, query: str, *args) -> list:
        return [query, *args]

    def test_create_table(self, monkeypatch):
        monkeypatch.setattr(
            self.test_driver, "_Driver__execute_query", self.execute_query
        )

        result = self.test_driver.create_table("testtable")

        assert None == result

    def test_create_index(self, monkeypatch):
        monkeypatch.setattr(
            self.test_driver, "_Driver__execute_query", self.execute_query
        )

        result = self.test_driver.create_index(table_name="testtable", fields=["id"])

        assert None == result

    def test_insert_document(self, monkeypatch):
        monkeypatch.setattr(
            self.test_driver, "_Driver__execute_query", self.execute_query
        )

        result = self.test_driver.insert_document(
            table_name="testtable", document={"id": 1, "name": "test"}
        )

        assert None == result

    def test_read_documents(self, monkeypatch):
        monkeypatch.setattr(
            self.test_driver, "_Driver__execute_query", self.execute_query
        )

        result = self.test_driver.read_documents(
            table_name="testtable", where_clause="1=1"
        )

        assert ["SELECT * FROM testtable WHERE 1=1"] == result

    def test_read_document_fields(self, monkeypatch):
        monkeypatch.setattr(
            self.test_driver, "_Driver__execute_query", self.execute_query
        )

        result = self.test_driver.read_document_fields(
            table_name="testtable", fields=["id", "name"], where_clause="1=1"
        )

        assert ["SELECT id,name FROM testtable WHERE 1=1"] == result

    def test_execute_custom_query(self, monkeypatch):
        monkeypatch.setattr(
            self.test_driver, "_Driver__execute_query", self.execute_query
        )

        result = self.test_driver.execute_custom_query(
            "UPDATE testtable SET name = ? WHERE id = ?", "test2", "1"
        )

        assert ["UPDATE testtable SET name = ? WHERE id = ?", "test2", "1"] == result

    def test_insert_account(self, monkeypatch):
        monkeypatch.setattr(
            self.test_driver, "_Driver__execute_query", self.execute_query
        )

        result = self.test_driver.insert_account(document={"id": 1, "name": "test"})

        assert None == result

    def test_insert_ledger(self, monkeypatch):
        monkeypatch.setattr(
            self.test_driver, "_Driver__execute_query", self.execute_query
        )

        result = self.test_driver.insert_ledger(document={"id": 1, "name": "test"})

        assert None == result

    def test_insert_journal_entry(self, monkeypatch):
        monkeypatch.setattr(
            self.test_driver, "_Driver__execute_query", self.execute_query
        )

        result = self.test_driver.insert_journal_entry(
            document={"id": 1, "name": "test"}
        )

        assert None == result
