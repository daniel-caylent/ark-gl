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

        return "Document"


    def read_document_fields(
        self, table_name: str, fields: list, where_clause: str = None
    ):
        """Read specific fields from a table"""

        return "field"


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
