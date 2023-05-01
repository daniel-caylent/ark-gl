import unittest
from unittest.mock import patch, Mock
import sys

sys.path.append('../../')

import app.v1.layers.database.python.database.fund_entity as fund_entity
import app.v1.layers.database.python.database.connection as connection
import app.v1.layers.database.python.database.db_main as db_main

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.db = "ARKGL"
    
    @patch(fund_entity.__name__+'.get_id', Mock(return_value=123))
    def test_get_id(self):
        result = fund_entity.get_id(self.db, None, '', '')

        self.assertEqual(result, 123)
    

    @patch(connection.__name__+'.get_connection', Mock(return_value=Mock()))
    @patch(db_main.__name__+'.execute_single_record_select', Mock(return_value={'uuid':'abcde', 'id':123, 'name':'account'}))
    def test_select_by_uuid(self):
        result = fund_entity.select_by_uuid(self.db, 'abcde', '', '')

        self.assertEqual(result, {'uuid':'abcde', 'id':123, 'name':'account'})


if __name__ == '__main__':
    unittest.main()
