from mock import Mock

from .report_test_base import ReportTestBase


class TestLineItem(ReportTestBase):
    trial_balance_input = {
        "journalEntryState": "POSTED",
        "hideZeroBalance": False,
        "ledgerId": [
            "32fd629e-bc96-11ed-8a31-0ed8d524c7fe",
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        ],
        "startDay": "2017-01-01",
        "endDay": "2017-05-31",
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

        result = report.select_trial_balance(self.db, self.trial_balance_input, "", "")

        assert [{"uuid": "abcde", "id": 123, "name": "account"}] == result
