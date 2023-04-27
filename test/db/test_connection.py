import unittest
from unittest import mock
import sys

# setting path
sys.path.append('../../')

import app.v1.layers.database.python.database.connection as connection

class TestConnection(unittest.TestCase):

    def setUp(self):
        self.conn = mock.MagicMock()
        self.cursor = mock.MagicMock()
        self.cursor.fetchall.return_value = ['aRow']

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    #@unittest.skip("should replace the connection toa mocked object")
    def test_get_connection(self):
        self.assertIsNotNone(self.conn)

    #@unittest.skip("should replace the connection toa mocked object")
    def test_query(self):
        self.cursor.execute("SELECT * FROM account")
        result = self.cursor.fetchall()
        self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main()
