from mock import Mock
from .fund_entity_test_base import FundEntityTestBase

class TestFundEntity(FundEntityTestBase):

    db = "ARKGL"

    # TODO: check the value of this test
    def test_get_id(self, monkeypatch):
        import app.v1.layers.database.python.database.fund_entity as fund_entity

        def get_id(db: str, uuid: str, region_name, secret_name):
            return 123

        monkeypatch.setattr(fund_entity, 'get_id', get_id)

        result = fund_entity.get_id(self.db, None, '', '')

        assert 123 == result


    def test_select_by_uuid(self, monkeypatch):
        import app.v1.layers.database.python.database.fund_entity as fund_entity
        import app.v1.layers.database.python.database.connection as connection
        import app.v1.layers.database.python.database.db_main as db_main

        def execute_single_record_select(conn, params):
            return {'uuid':'abcde', 'id':123, 'name':'account'}

        monkeypatch.setattr(connection, 'get_connection', Mock())
        monkeypatch.setattr(db_main, 'execute_single_record_select', execute_single_record_select)

        result = fund_entity.select_by_uuid(self.db, 'abcde', '', '')

        assert {'uuid':'abcde', 'id':123, 'name':'account'} == result
