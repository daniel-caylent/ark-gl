"""This module adapts specifc methods to access the QLDB database"""

from logging import getLogger
import botocore
from pyqldb.config.retry_config import RetryConfig
from pyqldb.driver.qldb_driver import QldbDriver
from pyqldb.cursor.buffered_cursor import BufferedCursor

logger = getLogger(__name__)

class Driver:
    """Driver to handle QLDB Ledgers access"""
    def __init__(
        self,
        ledger_name,
        retry_config=RetryConfig(retry_limit=0),
        config=botocore.config.Config(
            retries={"max_attempts": 0}, read_timeout=10, connect_timeout=10
        ),
        region_name=None,
        boto3_session=None,
    ):
        # Initialize the driver
        """Constructor of QLDB database class"""
        self.qldb_driver = QldbDriver(
            ledger_name=ledger_name,
            retry_config=retry_config,
            config=config,
            region_name=region_name,
            boto3_session=boto3_session if boto3_session else None,
        )


    def __execute_single_query(self, query: str, *args) -> BufferedCursor:
        """Private method for executing query"""
        cursor = self.qldb_driver.execute_lambda(
            lambda x: x.execute_statement(query, *args)
        )

        return cursor


    def __execute_transactional_query(self, query: str, documents: []) -> BufferedCursor:
        """Private method for executing query in a transactional manner"""
        def insert_documents(transaction_executor):
            for document in documents:
                transaction_executor.execute_statement(query, document)

        self.qldb_driver.execute_lambda(insert_documents)


    def create_table(self, table_name: str) -> None:
        """Create table method in qldb"""
        logger.info("Creating the table %s", table_name)
        query = "CREATE TABLE " + table_name
        self.__execute_single_query(query)


    def create_index(self, table_name: str, fields: list) -> None:
        """Create index method on qldb table"""
        fields_str = ",".join(fields)

        logger.info("Creating index on table %s to fields %s", table_name, fields_str)

        query = "CREATE INDEX ON " + table_name + "(" + fields_str + ")"

        self.__execute_single_query(query)


    def insert_document(self, table_name: str, document: dict) -> None:
        """Insert document method"""
        logger.info("Inserting a document into table %s", table_name)
        query = "INSERT INTO " + table_name + " ?"

        self.__execute_single_query(query, document)


    def insert_documents(self, table_name: str, documents: []) -> None:
        """Insert document method"""
        logger.info("Inserting a document into table %s", table_name)
        query = "INSERT INTO " + table_name + " ?"

        self.__execute_transactional_query(query, documents)


    def read_documents(
        self, table_name: str, where_clause: str = None
    ) -> BufferedCursor:
        """Read document method"""
        if where_clause:
            sql_query = "SELECT * FROM " + table_name + " WHERE " + where_clause
        else:
            sql_query = "SELECT * FROM " + table_name

        logger.info("Querying the table %s", table_name)

        cursor = self.__execute_single_query(sql_query)

        return cursor


    def read_document_fields(
        self, table_name: str, fields: list, where_clause: str = None
    ):
        """Read specific fields from a table"""
        if fields == []:
            fields_str = "*"
        else:
            fields_str = ",".join(fields)

        if where_clause:
            sql_query = (
                "SELECT "
                + fields_str
                + " FROM "
                + table_name
                + " WHERE "
                + where_clause
            )
        else:
            sql_query = "SELECT " + fields_str + " FROM " + table_name

        logger.info("Querying the table %s", table_name)

        cursor = self.__execute_single_query(sql_query)

        return cursor


    def execute_custom_query(self, sql_query: str, *args) -> BufferedCursor:
        """Execute a custom query on QLDB table"""
        logger.info("Executing custom query: %s", sql_query)
        cursor = self.__execute_single_query(sql_query, *args)

        return cursor


    def insert_account(self, document: dict) -> None:
        """Wrapper around account table for inserting document"""
        self.insert_document("account", document)


    def insert_many_accounts(self, documents: []) -> None:
        """Wrapper around account table for inserting many documents"""
        self.insert_documents("account", documents)


    def insert_ledger(self, document: dict) -> None:
        """Wrapper around ledge table for inserting document"""
        self.insert_document("ledger", document)


    def insert_many_ledgers(self, documents: []) -> None:
        """Wrapper around account table for inserting many documents"""
        self.insert_documents("ledger", documents)


    def insert_journal_entry(self, document: dict) -> None:
        """Wrapper around journal entry table for inserting document"""
        self.insert_document("journal_entry", document)


    def insert_many_journal_entries(self, documents: []) -> None:
        """Wrapper around account table for inserting many documents"""
        self.insert_documents("journal_entry", documents)
