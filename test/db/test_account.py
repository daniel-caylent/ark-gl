import unittest
from unittest.mock import patch, Mock
import sys

sys.path.append('../../')

import app.v1.layers.database.python.database.account as account
import app.v1.layers.database.python.database.connection as connection
import app.v1.layers.database.python.database.db_main as db_main

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.insert_input = {
            "accountNo": 778897,
            "fundId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
            "parentAccountNo": 1234567,
            "accountName": "Miscellaneous Expenses.",
            "accountDescription": "Miscellaneous Expenses is an aggregation account that includes all miscellaneous expenses including pizza and burritos.",
            "attributeNo": 2,
            "FSMappingId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
            "FSName": "FSMapping is used for reporting purposes.",
            "isTaxable": True,
            "isVendorCustomerPartnerRequired": False,
            "isDryRun": False
        }

        self.update_input = {
            "accountName": "Miscellaneous Expenses UPDATED 123",
            "FSName": "UPDATED: FSMapping is used for reporting purposes."
        }

        self.maxDiff = None

        self.db = "ARKGL"
    
    
    @patch(account.__name__+'.__get_insert_query')
    @patch(connection.__name__+'.get_connection')
    def test_insert(self, mock_connection, mock_get_query):
        mock_connection.return_value = Mock()
        mock_get_query.return_value = (None, None, 'asd-123-456')

        result = account.insert(self.db, self.insert_input, '', '')

        self.assertEqual(result, 'asd-123-456')
    

    @patch(account.__name__+'.__get_delete_query')
    @patch(connection.__name__+'.get_connection')
    def test_delete(self, mock_connection, mock_get_query):
        mock_connection.return_value = Mock()
        mock_get_query.return_value = (None, None)

        result = account.delete(self.db, 'asd-123-456', '', '')

        self.assertEqual(result, None)
    
    
    @patch(account.__name__+'.__get_update_query')
    @patch(connection.__name__+'.get_connection')
    def test_update(self, mock_connection, mock_get_query):
        mock_connection.return_value = Mock()
        mock_get_query.return_value = (None, None)

        result = account.update(self.db, 'asd-123-456', self.update_input, '', '')

        self.assertEqual(result, None)


    @patch(connection.__name__+'.get_connection', Mock(return_value=Mock()))
    @patch(db_main.__name__+'.execute_single_record_select', Mock(return_value={'uuid':'abcde', 'id':123, 'name':'account'}))
    def test_select_by_number(self):
        result = account.select_by_number(self.db, None, '', '')

        self.assertEqual(result, {'uuid':'abcde', 'id':123, 'name':'account'})
    

    @patch(account.__name__+'.select_by_number', Mock(return_value={'uuid':'abcde', 'id':123, 'name':'account'}))
    def test_get_id(self):
        result = account.get_id(self.db, None, '', '')

        self.assertEqual(result, 123)
    

    @patch(connection.__name__+'.get_connection', Mock(return_value=Mock()))
    @patch(db_main.__name__+'.execute_single_record_select', Mock(return_value={'uuid':'abcde', 'id':123, 'name':'account'}))
    def test_select_by_uuid(self):
        result = account.select_by_uuid(self.db, 'abcde', '', '')

        self.assertEqual(result, {'uuid':'abcde', 'id':123, 'name':'account'})
    

    @patch(connection.__name__+'.get_connection', Mock(return_value=Mock()))
    @patch(db_main.__name__+'.execute_multiple_record_select', Mock(return_value=[{'uuid':'abcde', 'id':123, 'name':'account'}]))
    def test_select_by_fund(self):
        result = account.select_by_fund(self.db, 'abcde', '', '')

        self.assertEqual(result, [{'uuid':'abcde', 'id':123, 'name':'account'}])
    

    @patch(connection.__name__+'.get_connection', Mock(return_value=Mock()))
    @patch(db_main.__name__+'.execute_single_record_select', Mock(return_value={'uuid':'abcde', 'id':123, 'name':'account'}))
    def test_select_by_name(self):
        result = account.select_by_name(self.db, 'abcde', '', '')

        self.assertEqual(result, {'uuid':'abcde', 'id':123, 'name':'account'})


if __name__ == '__main__':
    unittest.main()
