from .account_attributes_test_base import AccountAttributesTestBase

class TestAccountAttributes(AccountAttributesTestBase):

    insert_input = {
        "accountNo": 778897,
        "fundId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
        "parentAccountNo": 1234567,
        "accountName": "Miscellaneous Expenses.",
        "accountDescription": "Miscellaneous Expenses is an aggregation account that includes all miscellaneous expenses including pizza and burritos.",
        "attributeNo": 2,
        "FSMappingId": "fb84c7c6-9f62-11ed-8cf5-0ed4c7ff8d52",
        "FSName": "FSMapping is used for reporting purposes.",
        "isTaxable": True,
        "isVendorCustomerPartnerRequired": False
    }

    update_input = {
        "accountName": "Miscellaneous Expenses UPDATED 123",
        "FSName": "UPDATED: FSMapping is used for reporting purposes."
    }

    max_diff = None

    db = "ARKGL"

    def test_get_id(self, monkeypatch):

        import app.layers.database.python.database.account_attribute as account_attribute

        def mock_select_by_uuid(db, uuid, region_name, secret_name):
            return {
                'uuid': 'asd-123',
                'id': 123,
                'type': 'acct type 1'
            }

        monkeypatch.setattr(account_attribute, 'select_by_uuid', mock_select_by_uuid)

        result = account_attribute.get_id(self.db, 'asd-123', '', '')

        assert 123 == result
