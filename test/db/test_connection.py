import unittest
from unittest import mock
import sys

# setting path
sys.path.append('../')

import app.v1.layers.database.python.database.connection as connection

class TestConnection(unittest.TestCase):

    def setUp(self):
        self.conn = connection.get_connection(db_name='ARKGL', region_name='us-east-2', secret_name='ark/db-password')
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    @unittest.skip("should replace the connection toa mocked object")
    def test_get_connection(self):
        self.assertIsNotNone(self.conn)

    @unittest.skip("should replace the connection toa mocked object")
    def test_query(self):
        self.cursor.execute("SELECT * FROM account")
        result = self.cursor.fetchall()
        self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main()
