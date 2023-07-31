"""Mock QLDB Driver"""

class Driver:
    """Driver to handle QLDB Ledgers access"""
    def __init__(
        self,
        ledger_name,
        retry_config=None,
        config=None,
        region_name=None,
        boto3_session=None
    ):
        pass

    def __execute_single_query(self, query: str, *args):
        """Private method for executing query"""
        return (query, *args)


    def __execute_transactional_query(self, query: str, documents: []):
        """Private method for executing query in a transactional manner"""
        return None

    def create_table(self, table_name: str) -> None:
        """Create table method in qldb"""
        return None

    def create_index(self, table_name: str, fields: list) -> None:
        """Create index method on qldb table"""
        return None

    def insert_document(self, table_name: str, document: dict) -> None:
        """Insert document method"""
        return None

    def insert_documents(self, table_name: str, documents: []) -> None:
        """Insert document method"""
        return None

    def read_documents(
        self, table_name: str, where_clause: str = None
    ):
        """Read document method"""
        if table_name == "account":
            return [
                {
                    "id": 12142,
                    "account_no": "256495",
                    "uuid": "b8c0ca03-04ae-48e9-a36d-cabff658a721",
                    "fs_mapping_status": "UNMAPPED",
                    "fund_entity_id": "082453e7-64ce-41ad-b478-1c861fff8145",
                    "account_attribute_id": "4f5dd0ce-eb7e-11ed-9a6e-0a3efd619f29",
                    "parent_id": None,
                    "name": "Acct-ark-256-631",
                    "description": "ark 256",
                    "post_date": None,
                    "state": "UNUSED",
                    "is_hidden (int)": 0,
                    "created_at": "2023-07-31 17:56:12"
                }
            ]
        elif table_name == "ledger":
            return [
                {
                    "id": 130,
                    "uuid": "d9bc1a3f-0bb7-11ee-b49c-0a3efd619f29",
                    "fund_entity_id": "b5e9488f-24cb-4881-87df-b05f76cbe1b9",
                    "name": "Franco - Parent fdsfdfdas",
                    "description": "Franco parent, sub sub test",
                    "post_date": "2023-06-15 20:04:51",
                    "state": "POSTED",
                    "is_hidden": 0,
                    "currency": "USD",
                    "decimals": 2,
                    "created_at": "2023-06-15 20:04:35"
                }
            ]

        elif table_name == "journal_entry":
            return [
                {
                    "id": 282,
                    "journal_entry_num": 1,
                    "uuid": "df0f2420-0bbf-11ee-b49c-0a3efd619f29",
                    "ledger_id": "9876ce18-0bbe-11ee-b49c-0a3efd619f29",
                    "date": "2023-06-15",
                    "reference": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "memo": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "adjusting_journal_entry": 1,
                    "state": "POSTED",
                    "is_hidden": 0,
                    "post_date": "2023-06-15 21:02:14",
                    "created_at": "2023-06-15 21:02:00",
                    "currency": "EUR",
                    "decimals": 2,
                    "fund_entity_id": "c6bb22f3-e5d5-4192-b19b-1acc0c22a49f",
                    "line_items": [
                        {
                        "id": 2842,
                        "uuid": "df114736-0bbf-11ee-b49c-0a3efd619f29",
                        "account_id": "a16df5a0-0bbe-11ee-b49c-0a3efd619f29",
                        "account_no": "205",
                        "account_name": "If we calculate the microchip, we can get to the SQL array through the wireless PNG transmitter!",
                        "journal_entry_id": 282,
                        "line_number": 1,
                        "memo": "5aeb268f89e4d786d58ac87f1014ada3870276e9c1b235708330353a3b22b9c3",
                        "entity_id": "49dd9637-05da-4eec-98c9-bcbc5cbec2a4",
                        "posting_type": "CREDIT",
                        "amount": 6000,
                        "created_at": "2023-06-15 21:02:00"
                        },
                        {
                        "id": 2843,
                        "uuid": "df13e3f1-0bbf-11ee-b49c-0a3efd619f29",
                        "account_id": "a3b52965-0bbe-11ee-b49c-0a3efd619f29",
                        "account_no": "423",
                        "account_name": "The SAS capacitor is down, transmit the cross-platform pixel so we can compress the XML bandwidth!",
                        "journal_entry_id": 282,
                        "line_number": 2,
                        "memo": "b4080d9cefc1bb10af86f0b3715497b987cf93491f05297cabd6d2758b7ddabe",
                        "entity_id": "49dd9637-05da-4eec-98c9-bcbc5cbec2a4",
                        "posting_type": "DEBIT",
                        "amount": 2000,
                        "created_at": "2023-06-15 21:02:00"
                        },
                        {
                        "id": 2844,
                        "uuid": "df1591eb-0bbf-11ee-b49c-0a3efd619f29",
                        "account_id": "a3b52965-0bbe-11ee-b49c-0a3efd619f29",
                        "account_no": "423",
                        "account_name": "The SAS capacitor is down, transmit the cross-platform pixel so we can compress the XML bandwidth!",
                        "journal_entry_id": 282,
                        "line_number": 3,
                        "memo": "02e88073eba5e0bdcc2c27718bab05169af40a861f3003fd59415b766f046f91",
                        "entity_id": "49dd9637-05da-4eec-98c9-bcbc5cbec2a4",
                        "posting_type": "DEBIT",
                        "amount": 4000,
                        "created_at": "2023-06-15 21:02:00"
                        }
                    ],
                    "attachments": [
                        {
                        "id": 252,
                        "uuid": "This is the id",
                        "journal_entry_id": 282,
                        "memo": "3533550468585acb059f7fd8336d9f27e4a6ced3214dec3a5fd34d149c498c5d",
                        "created_at": "2023-06-15 21:02:00"
                        }
                    ]
                }
            ]


    def read_document_fields(
        self, table_name: str, fields: list, where_clause: str = None
    ):
        """Read specific fields from a table"""

        return [
            {"uuid": 1},
            {"uuid": 1},
            {"uuid": 1},
            {"uuid": 1},
            {"uuid": 1},
            {"uuid": 1},
            {"uuid": 1},
            {"uuid": 1},
            {"uuid": 1}
        ]


    def execute_custom_query(self, sql_query: str, *args):
        """Execute a custom query on QLDB table"""

        return (sql_query, *args)


    def insert_account(self, document: dict) -> None:
        """Wrapper around account table for inserting document"""
        return None


    def insert_many_accounts(self, documents: []) -> None:
        """Wrapper around account table for inserting many documents"""
        return None


    def insert_ledger(self, document: dict) -> None:
        """Wrapper around ledge table for inserting document"""
        return None


    def insert_many_ledgers(self, documents: []) -> None:
        """Wrapper around account table for inserting many documents"""
        return None


    def insert_journal_entry(self, document: dict) -> None:
        """Wrapper around journal entry table for inserting document"""
        return None

