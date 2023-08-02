from tests.test_base import TestBase

class TestAccountAttributes(TestBase([])):

    def test_get_id(self, monkeypatch):

        import app.layers.database.python.database.account_attribute as account_attribute

        def mock_select_by_uuid(db, uuid, region_name, secret_name):
            return {
                'uuid': 'asd-123',
                'id': 123,
                'type': 'acct type 1'
            }

        monkeypatch.setattr(account_attribute, 'select_by_uuid', mock_select_by_uuid)

        result = account_attribute.get_id("db", 'asd-123', '', '')

        assert 123 == result

    def test_select_by_uuid(self, monkeypatch):

        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account_attribute as account_attribute

        monkeypatch.setattr(connection, "get_connection", lambda *args: None)
        monkeypatch.setattr(db_main, "execute_single_record_select", lambda *args: None)

        account_attribute.select_by_uuid("db", 'MY_UUID', '', '')


    def test_select_all(self, monkeypatch):

        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account_attribute as account_attribute

        monkeypatch.setattr(connection, "get_connection", lambda *args: None)
        monkeypatch.setattr(db_main, "execute_multiple_record_select", lambda *args: [])

        account_attribute.select_all("db", '', '')
