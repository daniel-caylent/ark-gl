from tests.mock.db import MockCursor, MockConn

from .accounts_test_base import AccountsTestBase

MOCK_ACCOUNT_RECORD = {
    "uuid": "MOCK_UUID",
    "fund_entity_id": "",
    "client_id": "",
    "account_no": "",
    "state": "",
    "parent_id": "",
    "parent_name": "",
    "name": "",
    "description": "",
    "account_attribute_id": "",
    "is_taxable": "",
    "is_entity_required": "",
    "fs_mapping_id": "",
    "fs_mapping_name": "",
    "fs_name": "",
    "post_date": "",
    "fs_mapping_status": "",
}

MOCK_INPUT = {
        "accountNo": 778897,
        "fundId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
        "parentAccountId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
        "accountName": "Miscellaneous Expenses.",
        "accountDescription": "Miscellaneous Expenses is an aggregation account that includes all miscellaneous expenses including pizza and burritos.",
        "attributeId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
        "fsMappingId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
        "fsName": "FSMapping is used for reporting purposes.",
        "isTaxable": True,
        "isEntityRequired": False
    }

class TestAccount(AccountsTestBase):

    update_input = {
        "accountName": "Miscellaneous Expenses UPDATED 123",
        "FSName": "UPDATED: FSMapping is used for reporting purposes."
    }

    max_diff = None

    db = "ARKGL"


    def test_insert(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account_attribute as account_attribute


        monkeypatch.setattr(account_attribute, 'get_id', lambda *args: "ATT_ID")
        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)
        monkeypatch.setattr(db_main, 'get_new_uuid', lambda *args: "GENERATED UUID")

        result = account.insert("db", MOCK_INPUT, '', '')

        assert "GENERATED UUID" == result


    def test_delete(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account_attribute as account_attribute
        import app.layers.database.python.database.fund_entity as fund_entity


        monkeypatch.setattr(account_attribute, 'get_id', lambda *args: "ATT_ID")
        monkeypatch.setattr(fund_entity, 'get_id', lambda *args: "FUND_ID")
        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.delete("db", "TEST_ID", '', '')


    def test_update(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account_attribute as account_attribute


        monkeypatch.setattr(account_attribute, 'get_id', lambda *args: "ATT_ID")
        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.update("db", "TEST_ID", MOCK_INPUT, '', '')


    def test_select_by_uuid(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        result = account.select_by_uuid("db", "UUID", '', '')

        assert result["uuid"] == MOCK_ACCOUNT_RECORD["uuid"]


    def test_select_by_uuid_with_cursor(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(db_main, 'execute_single_record_select_with_cursor', lambda *args: MOCK_ACCOUNT_RECORD)

        result = account.select_by_uuid_with_cursor("db", "UUID", MockCursor())

        assert result["uuid"] == MOCK_ACCOUNT_RECORD["uuid"]


    def test_select_by_fund(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_ACCOUNT_RECORD])

        result = account.select_by_fund("db", "UUID", '', '')

        assert result[0]["uuid"] == MOCK_ACCOUNT_RECORD["uuid"]

    def test_bulk_delete(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.bulk_delete("db", ["TEST_ID"], '', '')


    def test_bulk_insert(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account_attribute as account_attribute


        monkeypatch.setattr(account_attribute, 'get_id', lambda *args: "ATT_ID")
        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.bulk_insert("db", [MOCK_INPUT, MOCK_INPUT], '', '')

    def test_select_count_with_post_date(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: {"count(*)": 1})

        account.select_count_with_post_date("db", '', '')

    def test_select_by_name_and_fund(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.select_by_name_and_fund("db", "acct_name", "fund_id", '', '')

    def test_get_id_by_name_and_fund(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.get_id_by_name_and_fund("db", "acct_name", "fund_id", '', '')


    def test_get_id_by_uuid(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.get_id_by_uuid("db", "UUID", '', '')


    def test_get_uuid_by_name_and_fund(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.get_uuid_by_name_and_fund("db", "acct_name", "fund_id", '', '')

    def test_select_committed_between_dates(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.select_committed_between_dates("db", "START_DATE", "END_DATE", '', '')


    def test_get_recursive_childs_by_uuids(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_ACCOUNT_RECORD])

        account.get_recursive_childs_by_uuids("db", ["UUID1", "UUID2"], '', '')


    def test_get_recursive_parents_by_uuids(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [MOCK_ACCOUNT_RECORD])

        account.get_recursive_parents_by_uuids("db", ["UUID1", "UUID2"], '', '')


    def test_bulk_update(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main


        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        mock_update = MOCK_INPUT
        mock_update["accountId"] = "Account UUID"

        account.bulk_update("db", [mock_update], '', '')

    # def test_commit(self, monkeypatch):
    #     import app.layers.database.python.database.account as account
    #     import app.layers.database.python.database.connection as connection
    #     import app.layers.database.python.database.db_main as db_main
    #     from app.layers.qldb.python.ark_qldb import post


    #     monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
    #     monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)
    #     monkeypatch.setattr(post, 'post', lambda *args: None)

    #     account.commit("db", "UUID", '', '')

    def test_bulk_state(self, monkeypatch):
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main


        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_ACCOUNT_RECORD)

        account.bulk_state("db", ["ID1", "ID2"], '', '')
    