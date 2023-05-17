from mock import MagicMock

from .connection_test_base import ConnectionTestBase

class TestConnection(ConnectionTestBase):

    conn = MagicMock()
    cursor = MagicMock()

    def test_get_connection(self):
        assert self.conn is not None

    def test_query(self, monkeypatch):

        def fetchall():
            return ['aRow']

        monkeypatch.setattr(self.cursor, 'fetchall', fetchall)

        self.cursor.execute("SELECT * FROM account")

        result = self.cursor.fetchall()

        assert 1 == len(result)
