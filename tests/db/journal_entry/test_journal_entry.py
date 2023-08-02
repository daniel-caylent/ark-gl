from tests.mock.db import MockConn, MockCursor

from .journal_entry_test_base import JournalEntryTestBase

MOCK_INPUT = {
    "ledgerId": "ledger-12345",
    "reference": "Transaction - 2023-01-30#007",
    "memo": "These charges describe catered lunches.",
    "adjustingJournalEntry": True,
    "attachments": [
        {
        "documentId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
        "documentMemo": "Scanned Receipt for Office Pizza Party."
        },
        {
        "documentId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e321",
        "documentMemo": "Scanned Receipt for Office Taco Party."
        }
    ],
    "lineItems": [
        {
            "lineItemNo": 1,
            "accountId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e321",
            "memo": "These charges describe catered Pizza.",
            "entityId": None,
            "amount": 10012000,
            "type": "CREDIT"
        },
        {
            "lineItemNo": 2,
            "accountId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e321",
            "memo": "These charges describe catered Pizza.",
            "entityId": None,
            "amount": 10012111,
            "type": "DEBIT"
        }
    ]
}

MOCK_RECORD = {
    "id": 1,
    "uuid": "UUID",
    "journal_entry_num": 5,
    "ledger_id": "",
    "reference": "",
    "memo": "",
    "adjusting_journal_entry": "",
    "state": "",
    "post_date": "",
    "date": "",
    "attachments": "",
    "line_items": "",
    "currency": "",
    "decimals": "",
    "fund_entity_id": "",
    "ledger_state": "",
    "account_state": "",
    "account_id": ""
}


class TestJournalEntry(JournalEntryTestBase):


    def test_insert(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.db_main as db_main


        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_RECORD)
        monkeypatch.setattr(db_main, 'get_new_uuid', lambda *args: "GENERATED UUID")
        monkeypatch.setattr(account, 'get_id_by_uuid', lambda *args: 1)

        result = journal_entry.insert("db", MOCK_INPUT, '', '')

        assert "GENERATED UUID" == result



    def test_delete(self, monkeypatch):
        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.connection as connection

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: {
                "journal_entry_num": 1
            })

        journal_entry.delete("db", 'journal-123456', '', '')



    def test_update(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account as account


        def record_get(*args):
            return {
                "journal_entry_num": 1
            }

        monkeypatch.setattr(account, 'get_id_by_uuid', lambda *args: 1)
        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', record_get)

        update = {
        "ledgerId": "ledger-12345"
    }

        journal_entry.update("db", "ID", update, '', '')

    def test_select_by_uuid(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account as account


        monkeypatch.setattr(account, 'get_id_by_uuid', lambda *args: 1)
        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_RECORD)

        journal_entry.select_by_uuid("db", "ID",'', '')

    def test_select_ids_by_uuid_list(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account as account


        monkeypatch.setattr(account, 'get_id_by_uuid', lambda *args: 1)
        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [
            {"uuid": "UUID", "id": 1},
            {"uuid": "UUID2", "id": 2}
        ])

        journal_entry.select_ids_by_uuid_list("db", ["ID1", "ID2"],'', '')


    def test_select_by_ledger_uuid(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account as account


        monkeypatch.setattr(account, 'get_id_by_uuid', lambda *args: 1)
        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [
            MOCK_RECORD, MOCK_RECORD
        ])

        journal_entry.select_by_ledger_uuid("db", "LEDGER_ID",'', '')


    def test_select_posted_between_dates(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account as account


        monkeypatch.setattr(account, 'get_id_by_uuid', lambda *args: 1)
        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [
            MOCK_RECORD, MOCK_RECORD
        ])

        journal_entry.select_posted_between_dates(
            "db", "date1",'date1', '', ''
        )


    def test_bulk_delete(self, monkeypatch):
        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.connection as connection

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [
                MOCK_RECORD, MOCK_RECORD
            ]
        )

        journal_entry.bulk_delete("db", ["UUID", "UUID"], '', '')


    def test_select_count_with_post_date(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: {
            "count(*)": 1
        })

        journal_entry.select_count_with_post_date(
            "db", '', ''
        )


    def test_select_max_number_by_ledger(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: {
            "journal_entry_num": 1
        })

        journal_entry.select_max_number_by_ledger(
            "db","LEDGER_ID", '', ''
        )

    def test_select_by_client_id(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: {
            "journal_entry_num": 1
        })

        journal_entry.select_by_client_id(
            "db","clientId", '', ''
        )

    def test_select_by_client_id_paginated(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: {
            "journal_entry_num": 1
        })

        journal_entry.select_by_client_id_paginated(
            "db","clientId", '', '', 1, 1
        )


    def test_select_max_number_by_ledger_with_cursor(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(db_main, 'execute_single_record_select_with_cursor', lambda *args: {
            "journal_entry_num": 1
        })

        journal_entry.select_max_number_by_ledger_with_cursor(
            "db","LEDGER_ID", MockCursor()
        )

    def test_bulk_insert(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.account as account
        import app.layers.database.python.database.db_main as db_main


        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: MOCK_RECORD)
        monkeypatch.setattr(db_main, 'get_new_uuid', lambda *args: "GENERATED UUID")
        monkeypatch.setattr(account, 'get_id_by_uuid', lambda *args: 1)


        monkeypatch.setattr(db_main, 'execute_single_record_select_with_cursor', lambda *args: {
            "journal_entry_num": 1
        })

        mock_input = [
            {
    "ledgerId": "ledger-12345",
    "reference": "Transaction - 2023-01-30#007",
    "memo": "These charges describe catered lunches.",
    "adjustingJournalEntry": True,
    "attachments": [
        {
        "documentId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e123",
        "documentMemo": "Scanned Receipt for Office Pizza Party."
        },
        {
        "documentId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e321",
        "documentMemo": "Scanned Receipt for Office Taco Party."
        }
    ],
    "lineItems": [
        {
            "lineItemNo": 1,
            "accountId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e321",
            "memo": "These charges describe catered Pizza.",
            "entityId": None,
            "amount": 10012000,
            "type": "CREDIT"
        },
        {
            "lineItemNo": 2,
            "accountId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e321",
            "memo": "These charges describe catered Pizza.",
            "entityId": None,
            "amount": 10012111,
            "type": "DEBIT"
        }
    ]
}
        ]

        result = journal_entry.bulk_insert("db", mock_input, '', '')

        assert "GENERATED UUID" == result[0]



    def test_select_by_uuid_with_cursor(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(db_main, 'execute_single_record_select_with_cursor', lambda *args: {
            "journal_entry_num": 1
        })

        journal_entry.select_by_uuid_with_cursor(
            "db","UUID", MockCursor()
        )

    def test_select_with_filter_paginated(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_single_record_select', lambda *args: {
            "journal_entry_num": 1
        })

        mock_filter = {
            "fundId": "id",
            "clientId": "id",
            "ledgerIds": ["id"],
            "entityIds": ["id"],
            "accountIds": ["id"]
        }

        journal_entry.select_with_filter_paginated(
            "db", mock_filter, '', '', 1, 1
        )

    def test_select_numbers_by_ledger_uuid(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [{
            "journal_entry_num": 1
        }])

        journal_entry.select_numbers_by_ledger_uuid(
            "db","ledger_id", '', ''
        )

    def test_select_draft_accounts_and_ledgers_by_id_list(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main

        monkeypatch.setattr(connection, 'get_connection', lambda *args: MockConn())
        monkeypatch.setattr(db_main, 'execute_multiple_record_select', lambda *args: [{
            "journal_entry_num": 1
        }])

        journal_entry.select_draft_accounts_and_ledgers_by_id_list(
            "db", ["ledger_id"], '', ''
        )

    
