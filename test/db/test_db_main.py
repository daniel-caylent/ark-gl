import unittest
from unittest.mock import patch
import sys

sys.path.append('../../')

import app.v1.layers.database.python.database.db_main as db_main

class TestDbMain(unittest.TestCase):
    def setUp(self):
        self.app_to_db = {
            'appId': 'db_id',
            'appName': 'db_name',
            'appEmail': 'db_email'
        }

    def test_trans_app_to_db(self):
        input = {
            'appId': 1,
            'appName': 'ark name',
            'appEmail': 'ark.pes@ark.com'
        }
        result = db_main.translate_to_db(self.app_to_db, input)
        self.assertEqual(
            result,
            {
                'db_id': 1,
                'db_name': 'ark name',
                'db_email': 'ark.pes@ark.com'
            }
        )
    
    def test_trans_db_to_app(self):
        input = {
            'db_id': 1,
            'db_name': 'ark name',
            'db_email': 'ark.pes@ark.com'
        }
        result = db_main.translate_to_app(self.app_to_db, input)
        self.assertEqual(
            result,
            {
                'appId': 1,
                'appName': 'ark name',
                'appEmail': 'ark.pes@ark.com'
            }
        )
    
    @patch(db_main.__name__)
    def test_get_new_uuid(self, mock_maindb):
        input = 'd559fa87-e51a-11ed-aede-0247c1ed2eeb'

        mock_maindb.get_new_uuid.return_value = 'd559fa87-e51a-11ed-aede-0247c1ed2eeb'

        self.assertEqual(mock_maindb.get_new_uuid.return_value, input)
    
    @patch(db_main.__name__)
    def test_select_single_record(self, mock_maindb):
        mock_maindb.execute_single_record_select.return_value = {'id':1, 'account_name':'account'}

        self.assertEqual(type(mock_maindb.execute_single_record_select.return_value), dict)
    
    @patch(db_main.__name__)
    def test_select_multiple_records(self, mock_maindb):
        mock_maindb.execute_multiple_record_select.return_value = [
            {'id':1, 'account_name':'account1'},
            {'id':2, 'account_name':'account2'},
            {'id':3, 'account_name':'account3'},
        ]
        self.assertEqual(type(mock_maindb.execute_multiple_record_select.return_value), list)
        self.assertGreaterEqual(len(mock_maindb.execute_multiple_record_select.return_value), 1)

if __name__ == '__main__':
    unittest.main()
