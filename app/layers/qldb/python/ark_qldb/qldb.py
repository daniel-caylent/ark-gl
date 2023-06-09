"""This module adapts specifc methods to access the QLDB database"""

from logging import getLogger
import botocore
from pyqldb.config.retry_config import RetryConfig
from pyqldb.driver.qldb_driver import QldbDriver
from pyqldb.cursor.buffered_cursor import BufferedCursor

logger = getLogger(__name__)


class Driver:
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
        self.qldb_driver = QldbDriver(
            ledger_name=ledger_name,
            retry_config=retry_config,
            config=config,
            region_name=region_name,
            boto3_session=boto3_session if boto3_session else None,
        )

    def __execute_query(self, query: str, *args) -> BufferedCursor:
        cursor = self.qldb_driver.execute_lambda(
            lambda x: x.execute_statement(query, *args)
        )

        return cursor

    def create_table(self, table_name: str) -> None:
        logger.info("Creating the table %s", table_name)
        query = "CREATE TABLE " + table_name
        self.__execute_query(query)

    def create_index(self, table_name: str, fields: list) -> None:
        fields_str = ",".join(fields)

        logger.info(
            "Creating index on table %s to fields %s",
            table_name,
            fields_str
        )

        query = "CREATE INDEX ON " + table_name + "(" + fields_str + ")"

        self.__execute_query(query)

    def insert_document(self, table_name: str, document: dict) -> None:
        logger.info("Inserting a document into table %s", table_name)
        query = "INSERT INTO " + table_name + " ?"
        self.__execute_query(query, document)

    def read_documents(
        self, table_name: str, where_clause: str = None
    ) -> BufferedCursor:
        if where_clause:
            sql_query = "SELECT * FROM " + table_name + " WHERE " + where_clause
        else:
            sql_query = "SELECT * FROM " + table_name

        logger.info("Querying the table %s", table_name)

        cursor = self.__execute_query(sql_query)

        return cursor

    def read_document_fields(
        self, table_name: str, fields: list, where_clause: str = None
    ):
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

        cursor = self.__execute_query(sql_query)

        return cursor

    def execute_custom_query(self, sql_query: str, *args) -> BufferedCursor:
        logger.info("Executing custom query: %s", sql_query)
        cursor = self.__execute_query(sql_query, *args)

        return cursor

    def insert_account(self, document: dict) -> None:
        self.insert_document("account", document)

    def insert_ledger(self, document: dict) -> None:
        self.insert_document("ledger", document)

    def insert_journal_entry(self, document: dict) -> None:
        self.insert_document("journal_entry", document)
