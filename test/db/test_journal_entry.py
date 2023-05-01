import unittest
from unittest.mock import patch, Mock
import sys

sys.path.append('../../')

import app.v1.layers.database.python.database.journal_entry as journal_entry
import app.v1.layers.database.python.database.line_item as line_item
import app.v1.layers.database.python.database.connection as connection
import app.v1.layers.database.python.database.db_main as db_main

class TestJournalEntry(unittest.TestCase):
    def setUp(self):
        self.insert_input = {
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

        self.update_input = {
            "ledgerId": "ledger-12345",
            "debitEntries": [
                {
                    "lineItemNo": 1,
                    "accountNo": 778899,
                    "entryMemo": "These charges describe catered Burgers."
                }
            ]
        }

        self.maxDiff = None

        self.db = "ARKGL"
    

    @patch(line_item.__name__+'.get_insert_query')
    @patch(journal_entry.__name__+'.__get_insert_query')
    @patch(connection.__name__+'.get_connection')
    def test_insert(self, mock_connection, mock_get_query, mock_line_item):
        mock_connection.return_value = Mock()
        mock_get_query.return_value = (None, None, 'journal-123456')
        mock_line_item.return_vaue = (None, None)

        result = journal_entry.insert(self.db, self.insert_input, '', '')

        self.assertEqual(result, 'journal-123456')
    

    @patch(line_item.__name__+'.get_delete_by_journal_query')
    @patch(journal_entry.__name__+'.__get_delete_query')
    @patch(connection.__name__+'.get_connection')
    def test_delete(self, mock_connection, mock_get_query, mock_line_item):
        mock_connection.return_value = Mock()
        mock_get_query.return_value = (None, None)
        mock_line_item.return_vaue = (None, None)

        result = journal_entry.delete(self.db, 'journal-123456', '', '')

        self.assertEqual(result, None)
    

    @patch(line_item.__name__+'.select_numbers_by_journal')
    @patch(line_item.__name__+'.get_update_query')
    @patch(journal_entry.__name__+'.__get_update_query')
    @patch(connection.__name__+'.get_connection')
    def test_update(self, mock_connection, mock_get_query, mock_line_item_update_query, mock_line_item_numbers):
        mock_connection.return_value = Mock()
        mock_get_query.return_value = (None, None)
        mock_line_item_update_query.return_vaue = (None, None)
        mock_line_item_numbers.return_value = [{"line_number": 1, "data": "test"}, {"line_number": 2, "data": "test2"}]

        result = journal_entry.update(self.db, 'journal-123456', self.update_input, '', '')

        self.assertEqual(result, None)
    
    
    @patch(connection.__name__+'.get_connection', Mock(return_value=Mock()))
    @patch(db_main.__name__+'.execute_single_record_select', Mock(return_value={'uuid':'abcde', 'id':123, 'name':'account'}))
    def test_select_by_uuid(self):
        result = journal_entry.select_by_uuid(self.db, 'abcde', '', '')

        self.assertEqual(result, {'uuid':'abcde', 'id':123, 'name':'account'})

if __name__ == '__main__':
    unittest.main()
