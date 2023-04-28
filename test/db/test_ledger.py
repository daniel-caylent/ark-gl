import unittest
from unittest.mock import patch, Mock
import sys

sys.path.append('../../')

import app.v1.layers.database.python.database.ledger as ledger
import app.v1.layers.database.python.database.fund_entity as fund_entity
import app.v1.layers.database.python.database.account_attribute as account_attribute
import app.v1.layers.database.python.database.connection as connection
import app.v1.layers.database.python.database.db_main as db_main

class TestLedger(unittest.TestCase):
    def setUp(self):
        self.insert_input = {
            "GLName": "Primary USD based General Ledger",
            "GLDescription": "The details surrounding this specialized General Ledger are beyond the scope of this documentation exercise.",
            "currencyName": "USD",
            "currencyDecimal": 2,
            "isHidden": False
        }

        self.update_input = {
            "GLName": "Primary ARS based General Ledger",
            "GLDescription": "The details General Ledger.",
        }

        self.maxDiff = None

        self.db = "ARKGL"
    
    @patch(ledger.__name__+'.__get_insert_query')
    @patch(connection.__name__+'.get_connection')
    def test_insert(self, mock_connection, mock_get_query):
        mock_connection.return_value = Mock()
        mock_get_query.return_value = (None, None, 'asd-123-456')

        result = ledger.insert(self.db, self.insert_input, '', '')

        self.assertEqual(result, 'asd-123-456')
    

    @patch(ledger.__name__+'.__get_delete_query')
    @patch(connection.__name__+'.get_connection')
    def test_delete(self, mock_connection, mock_get_query):
        mock_connection.return_value = Mock()
        mock_get_query.return_value = (None, None)

        result = ledger.delete(self.db, 'asd-123-456', '', '')

        self.assertEqual(result, None)
    

    @patch(ledger.__name__+'.__get_update_query')
    @patch(connection.__name__+'.get_connection')
    def test_update(self, mock_connection, mock_get_query):
        mock_connection.return_value = Mock()
        mock_get_query.return_value = (None, None)

        result = ledger.update(self.db, 'asd-123-456', self.update_input, '', '')

        self.assertEqual(result, None)

    @patch(ledger.__name__+'.select_by_uuid', Mock(return_value={'uuid':'abcde', 'id':123, 'name':'ledger'}))
    def test_get_id(self):
        result = ledger.get_id(self.db, None, '', '')
        self.assertEqual(result, 123)
    

    @patch(connection.__name__+'.get_connection', Mock(return_value=Mock()))
    @patch(db_main.__name__+'.execute_single_record_select', Mock(return_value={'uuid':'abcde', 'id':123, 'name':'ledger'}))
    def test_select_by_uuid(self):
        result = ledger.select_by_uuid(self.db, 'abcde', '', '')

        self.assertEqual(result, {'uuid':'abcde', 'id':123, 'name':'ledger'})
    

if __name__ == '__main__':
    unittest.main()
