import unittest
from unittest.mock import patch, Mock
import sys

sys.path.append('../../')

import app.v1.layers.database.python.database.account as account
from app.v1.layers.database.python.database.account import __get_insert_query as get_insert_query
from app.v1.layers.database.python.database.account import __get_update_query as get_update_query
from app.v1.layers.database.python.database.account import __get_delete_query as get_delete_query
import app.v1.layers.database.python.database.fund_entity as fund_entity
import app.v1.layers.database.python.database.account_attribute as account_attribute
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
    

    @patch(fund_entity.__name__+'.get_id', Mock(return_value=5))
    @patch(account_attribute.__name__+'.get_id', Mock(return_value=10))
    @patch(connection.__name__+'.get_connection', Mock(return_value=Mock()))
    @patch(db_main.__name__+'.get_new_uuid', Mock(return_value="d559fa87-e51a-11ed-aede-0247c1ed2eeb"))
    def test_get_insert_query(self):
        result = get_insert_query(self.db, self.insert_input, '', '')

        wanted_result = (
            """
        INSERT INTO """
        + self.db
        + """.account
            (uuid, account_no, fund_entity_id, account_attribute_id, parent_id, name, description,
            state, is_hidden, is_taxable, is_vendor_customer_partner_required)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s);""",
            (
                "d559fa87-e51a-11ed-aede-0247c1ed2eeb", self.insert_input["accountNo"], 5, 10, self.insert_input["parentAccountNo"],
                self.insert_input["accountName"], self.insert_input["accountDescription"], None, None,
                self.insert_input["isTaxable"], self.insert_input["isVendorCustomerPartnerRequired"]
            ),
            "d559fa87-e51a-11ed-aede-0247c1ed2eeb"
        )

        self.assertEqual(result, wanted_result)
    
    
    def test_get_update_query(self):
        id = "d559fa87-e51a-11ed-aede-0247c1ed2eeb"
        result = get_update_query(self.db, id, self.update_input)
        
        update_query = (
        """
        UPDATE """
        + self.db
        + """.account
        SET """
        )
        where_clause = "WHERE uuid = %s;"
        set_clause = "name = %s,\n"
        set_clause += "fs_name = %s\n "

        wanted_result = (
            update_query+set_clause+where_clause,
            (
                self.update_input["accountName"], self.update_input["FSName"], id
            )
        )

        self.assertEqual(result, wanted_result)


    def test_delete_query(self):
        id = "d559fa87-e51a-11ed-aede-0247c1ed2eeb"
        result = get_delete_query(self.db, id)
         
        wanted_result = (
        """
        DELETE FROM """
        + self.db
        + """.account
        WHERE uuid = %s;"""
        , (id,))

        self.assertEqual(result, wanted_result)
    

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
