import unittest
from unittest.mock import patch
import sys

sys.path.append('../../')

import app.v1.layers.database.python.database.account_attribute as account_attribute

class TestAccountAttribute(unittest.TestCase):
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
    

    def test_get_all(self):
        desired_output = (
        """
        SELECT accatt.id as attributeNo, acctyp.name as accountType, accatt.detail_type as detailType
        FROM """
        + self.db
        + """.account_attribute accatt
        INNER JOIN """
        + self.db
        + """.account_type acctyp ON (accatt.account_type_id = acctyp.id);"""
        )

        result = account_attribute.get_all(self.db)

        self.assertEqual(result, (desired_output, None))
    

    @patch(account_attribute.__name__+'.select_by_uuid')
    def test_get_id(self, account_attr_mock):
        account_attr_mock.return_value = {
            'uuid': 'asd-123',
            'id': 123,
            'type': 'acct type 1'
        }

        result = account_attribute.get_id(self.db, 'asd-123', '', '')

        self.assertEqual(result, 123)


if __name__ == '__main__':
    unittest.main()
