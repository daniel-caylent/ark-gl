from mock import Mock

from .report_test_base import ReportTestBase


class TestLineItem(ReportTestBase):
    trial_balance_input = {
        "journalEntryState": "POSTED",
        "ledgerIds": [
            "32fd629e-bc96-11ed-8a31-0ed8d524c7fe",
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        ],
        "startDate": "2017-01-01",
        "enddate": "2017-05-31",
        "accountIds": ["id"],
        "attributeIds": ["id"]
    }

    db = "ARKGL"

    def test_trial_balance(self, monkeypatch):
        import app.layers.database.python.database.report as report
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.connection as connection

        def execute_multiple_record_select(conn, params):
            return [{"uuid": "abcde", "id": 123, "name": "account"}]

        monkeypatch.setattr(
            db_main, "execute_multiple_record_select", execute_multiple_record_select
        )
        monkeypatch.setattr(connection, "get_connection", Mock())

        result = report.select_trial_balance("db", self.trial_balance_input, "", "")

        assert [{"uuid": "abcde", "id": 123, "name": "account"}] == result

    def test_trial_balance_detail(self, monkeypatch):
        import app.layers.database.python.database.report as report
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.connection as connection

        def execute_multiple_record_select(conn, params):
            return [{"uuid": "abcde", "id": 123, "name": "account"}]

        monkeypatch.setattr(
            db_main, "execute_multiple_record_select", execute_multiple_record_select
        )
        monkeypatch.setattr(connection, "get_connection", Mock())

        result = report.select_trial_balance_detail("db", self.trial_balance_input, "", "")

        assert [{"uuid": "abcde", "id": 123, "name": "account"}] == result

    def test_select_start_balance(self, monkeypatch):
        import app.layers.database.python.database.report as report
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.connection as connection


        monkeypatch.setattr(
            db_main, "execute_single_record_select", lambda *args: {"value": 0}
        )
        monkeypatch.setattr(connection, "get_connection", Mock())

        report.select_start_balance("db", "id","date", "", "")


    def test_select_end_balance(self, monkeypatch):
        import app.layers.database.python.database.report as report
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.connection as connection


        monkeypatch.setattr(
            db_main, "execute_single_record_select", lambda *args: {"value": 0}
        )
        monkeypatch.setattr(connection, "get_connection", Mock())

        report.select_end_balance("db", "id","date", "", "")

    
    # def test_balance_sheet(self, monkeypatch):
    #     import app.layers.database.python.database.report as report
    #     import app.layers.database.python.database.db_main as db_main
    #     import app.layers.database.python.database.connection as connection

    #     def execute_multiple_record_select(conn, params):
    #         return [{"uuid": "abcde", "id": 123, "name": "account"}]

    #     monkeypatch.setattr(
    #         db_main, "execute_multiple_record_select", execute_multiple_record_select
    #     )
    #     monkeypatch.setattr(connection, "get_connection", Mock())

    #     result = report.select_balance_sheet("db", self.trial_balance_input, "", "")

    #     assert [{"uuid": "abcde", "id": 123, "name": "account"}] == result

    # def test_income_statement(self, monkeypatch):
    #     import app.layers.database.python.database.report as report
    #     import app.layers.database.python.database.db_main as db_main
    #     import app.layers.database.python.database.connection as connection

    #     def execute_multiple_record_select(conn, params):
    #         return [{"uuid": "abcde", "id": 123, "name": "account"}]

    #     monkeypatch.setattr(
    #         db_main, "execute_multiple_record_select", execute_multiple_record_select
    #     )
    #     monkeypatch.setattr(connection, "get_connection", Mock())

    #     result = report.select_income_statement("db", self.trial_balance_input, "", "")

    #     assert [{"uuid": "abcde", "id": 123, "name": "account"}] == result

    # def test_1099(self, monkeypatch):
    #     import app.layers.database.python.database.report as report
    #     import app.layers.database.python.database.db_main as db_main
    #     import app.layers.database.python.database.connection as connection

    #     def execute_multiple_record_select(conn, params):
    #         return [{"uuid": "abcde", "id": 123, "name": "account"}]

    #     monkeypatch.setattr(
    #         db_main, "execute_multiple_record_select", execute_multiple_record_select
    #     )
    #     monkeypatch.setattr(connection, "get_connection", Mock())

    #     result = report.select_1099("db", self.trial_balance_input, "", "")

    #     assert [{"uuid": "abcde", "id": 123, "name": "account"}] == result
    
    # def test_1099_detail(self, monkeypatch):
    #     import app.layers.database.python.database.report as report
    #     import app.layers.database.python.database.db_main as db_main
    #     import app.layers.database.python.database.connection as connection

    #     def execute_multiple_record_select(conn, params):
    #         return [{"uuid": "abcde", "id": 123, "name": "account"}]

    #     monkeypatch.setattr(
    #         db_main, "execute_multiple_record_select", execute_multiple_record_select
    #     )
    #     monkeypatch.setattr(connection, "get_connection", Mock())

    #     result = report.select_1099_detail("db", self.trial_balance_input, "", "")

    #     assert [{"uuid": "abcde", "id": 123, "name": "account"}] == result

    # def test_1099_detail_balance(self, monkeypatch):
    #     import app.layers.database.python.database.report as report
    #     import app.layers.database.python.database.db_main as db_main
    #     import app.layers.database.python.database.connection as connection

    #     def execute_multiple_record_select(conn, params):
    #         return [{"uuid": "abcde", "id": 123, "name": "account"}]

    #     monkeypatch.setattr(
    #         db_main, "execute_multiple_record_select", execute_multiple_record_select
    #     )
    #     monkeypatch.setattr(connection, "get_connection", Mock())

    #     result = report.select_1099_detail_balance("db", self.trial_balance_input, "", "")

    #     assert [{"uuid": "abcde", "id": 123, "name": "account"}] == result
