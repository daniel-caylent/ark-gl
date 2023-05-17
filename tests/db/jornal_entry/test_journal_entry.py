from mock import Mock
from .jornal_entry_test_base import JornalEntryTestBase

class TestJournalEntry(JornalEntryTestBase):
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
        "debitEntries": [
            {
                "lineItemNo": 1,
                "accountNo": 778899,
                "entryMemo": "These charges describe catered Pizza.",
                "VendorCustomerPartner": {
                    "VCPtype": "Vendor",
                    "VCPId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524ffff"
                },
                "amount": 10012
            }
        ],
        "creditEntries": [
            {
                "lineItemNo": 2,
                "accountNo": 338899,
                "entryMemo": "These charges describe catered Pizza.",
                "VendorCustomerPartner": {
                    "VCPtype": "Vendor",
                    "VCPId": "fb84c7c6-9f62-11ed-8cf5-0ed8d524ffff"
                },
                "amount": 10012
            }
        ],
        "isHidden": False
    }

    update_input = {
        "ledgerId": "ledger-12345",
        "debitEntries": [
            {
                "lineItemNo": 1,
                "accountNo": 778899,
                "entryMemo": "These charges describe catered Burgers."
            }
        ]
    }

    max_diff = None

    db = "ARKGL"

    def test_insert(self, monkeypatch):
        import app.v1.layers.database.python.database.journal_entry as journal_entry
        import app.v1.layers.database.python.database.line_item as line_item
        import app.v1.layers.database.python.database.connection as connection

        def get_inserted_query(db, debit_entry, journal_entry_id, type, region_name, secret_name):
            return (None, None)

        def get_insert_query_jornal_entry(db, input, region_name, secret_name):
            return (None, None, 'journal-123456')

        monkeypatch.setattr(line_item, 'get_insert_query', get_inserted_query)
        monkeypatch.setattr(journal_entry, '__get_insert_query', get_insert_query_jornal_entry)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = journal_entry.insert(self.db, self.insert_input, '', '')

        assert 'journal-123456' == result


    def test_delete(self, monkeypatch):
        import app.v1.layers.database.python.database.journal_entry as journal_entry
        import app.v1.layers.database.python.database.line_item as line_item
        import app.v1.layers.database.python.database.connection as connection

        def get_delete_by_journal_query(db, id, region_name, secret_name):
            return (None, None)

        def get_delete_query_jornal_entry(db, uuid):
            return (None, None, 'journal-123456')

        monkeypatch.setattr(line_item, 'get_delete_by_journal_query', get_delete_by_journal_query)
        monkeypatch.setattr(journal_entry, '__get_delete_query', get_delete_query_jornal_entry)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = journal_entry.delete(self.db, 'journal-123456', '', '')

        assert None == result


    def test_update(self, monkeypatch):

        import app.v1.layers.database.python.database.journal_entry as journal_entry
        import app.v1.layers.database.python.database.line_item as line_item
        import app.v1.layers.database.python.database.connection as connection

        def select_numbers_by_journal(db, id, region_name, secret_name):
            return [{"line_number": 1, "data": "test"}, {"line_number": 2, "data": "test2"}]

        def get_update_query(db, line_uuid, debit_entry):
            return (None, None)

        def get_update_query_jornal_entry(db, uuid, input, region_name, secret_name):
            return (None, None, 'journal-123456')

        monkeypatch.setattr(line_item, 'select_numbers_by_journal', select_numbers_by_journal)
        monkeypatch.setattr(line_item, 'get_update_query', get_update_query)
        monkeypatch.setattr(journal_entry, '__get_update_query', get_update_query_jornal_entry)
        monkeypatch.setattr(connection, 'get_connection', Mock())

        result = journal_entry.update(self.db, 'journal-123456', self.update_input, '', '')

        assert None == result