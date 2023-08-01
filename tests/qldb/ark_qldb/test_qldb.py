from tests.test_base import TestBase
from tests.utils import APP_ARK_QLDB_LAYER

from  app.layers.qldb.python.ark_qldb.qldb import Driver

class MockDriver(Driver):
    def _Driver__execute_single_query(self, query: str, *args) -> list:
        return [query, *args]

class TestQldb(TestBase([APP_ARK_QLDB_LAYER])):

    def test_create_table(self):
        pass
        test_driver = MockDriver(None, None, None, None, None)

        result = test_driver.create_table("testtable")
        assert None == result

    def test_create_index(self):
        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.create_index(table_name="testtable", fields=["id"])

        assert None == result

    def test_insert_document(self):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.insert_document(
            table_name="testtable", document={"id": 1, "name": "test"}
        )

        assert None == result

    def test_read_documents(self):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.read_documents(
            table_name="testtable", where_clause="1=1"
        )

        assert ["SELECT * FROM testtable WHERE 1=1"] == result

    def test_read_document_fields(self):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.read_document_fields(
            table_name="testtable", fields=["id", "name"], where_clause="1=1"
        )

        assert ["SELECT id,name FROM testtable WHERE 1=1"] == result

    def test_execute_custom_query(self):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.execute_custom_query(
            "UPDATE testtable SET name = ? WHERE id = ?", "test2", "1"
        )

        assert ["UPDATE testtable SET name = ? WHERE id = ?", "test2", "1"] == result

    def test_insert_account(self):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.insert_account(document={"id": 1, "name": "test"})

        assert None == result

    def test_insert_ledger(self):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.insert_ledger(document={"id": 1, "name": "test"})

        assert None == result

    def test_insert_journal_entry(self):

        test_driver = MockDriver(None, None, None, None, None)
        result = test_driver.insert_journal_entry(
            document={"id": 1, "name": "test"}
        )

        assert None == result
