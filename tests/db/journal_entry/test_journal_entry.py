from mock import Mock
from .journal_entry_test_base import JournalEntryTestBase

class TestJournalEntry(JournalEntryTestBase):
    insert_input = {
        "ledgerId": "ledger-12345",
        "txReference": "Transaction - 2023-01-30#007",
        "txMemo": "These charges describe catered lunches.",
        "adjustingJournalEntry": True,
        "journalAttachments": [
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
                "amount": 10012,
                "type": "CREDIT"
            },
            {
                "lineItemNo": 2,
                "accountId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524e321",
                "memo": "These charges describe catered Pizza.",
                "entityId": None,
                "amount": 10012,
                "type": "DEBIT"
            }
        ]
    }

    update_input = {
        "ledgerId": "ledger-12345"
    }

    max_diff = None

    db = "ARKGL"

    def test_insert(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.line_item as line_item
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.account as account
         
        def account_get_by_uuid(*args):
            return 1
        
        def get_insert_query_journal_entry(db, input, region_name, secret_name):
            return (None, None, 'journal-123456')

        monkeypatch.setattr(account, 'get_id_by_uuid', account_get_by_uuid)
        monkeypatch.setattr(journal_entry, '__get_insert_query', get_insert_query_journal_entry)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = journal_entry.insert(self.db, self.insert_input, '', '')

        assert 'journal-123456' == result


    def test_delete(self, monkeypatch):
        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.line_item as line_item
        import app.layers.database.python.database.connection as connection

        def get_delete_by_journal_query(db, id):
            return (None, None)

        def get_delete_query_journal_entry(db, uuid):
            return (None, None, 'journal-123456')

        monkeypatch.setattr(line_item, 'get_delete_by_journal_query', get_delete_by_journal_query)
        monkeypatch.setattr(journal_entry, '__get_delete_query', get_delete_query_journal_entry)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = journal_entry.delete(self.db, 'journal-123456', '', '')

        assert None == result


    def test_update(self, monkeypatch):

        import app.layers.database.python.database.journal_entry as journal_entry
        import app.layers.database.python.database.line_item as line_item
        import app.layers.database.python.database.connection as connection
        import app.layers.database.python.database.db_main as db_main
        import app.layers.database.python.database.account as account

        def select_numbers_by_journal(db, id, region_name, secret_name):
            return [{"line_number": 1, "data": "test"}, {"line_number": 2, "data": "test2"}]

        def record_get(*args):
            return {
                "journal_entry_num": 1
            }
        def account_get_by_uuid(*args):
            return 1

        monkeypatch.setattr(line_item, 'select_numbers_by_journal', select_numbers_by_journal)
        monkeypatch.setattr(account, 'get_id_by_uuid', account_get_by_uuid)
        monkeypatch.setattr(connection, 'get_connection', Mock())
        monkeypatch.setattr(db_main, 'execute_single_record_select', record_get)

        result = journal_entry.update(self.db, 'journal-123456', self.update_input, '', '')

        assert None == result