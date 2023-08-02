class MockConn:
    def cursor(self, *args):
        return MockCursor()
    def commit(self):
        return None
    def rollback(self):
        return None

class MockCursor:
    def execute(self, *args, **kwargs):
        return None
    def fetchone(self):
        return {"acc_le_count": 1}
    def lastrowid(self):
        return 5
    def close(self):
        return None
    def fetchall(self):
        return []
    def executemany(self, *args):
        return None

