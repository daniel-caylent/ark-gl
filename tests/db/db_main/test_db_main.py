from .db_main_test_base import DbMainTestBase

class TestDbMain(DbMainTestBase):
    app_to_db = {
        'appId': 'db_id',
        'appName': 'db_name',
        'appEmail': 'db_email'
    }

    def test_trans_app_to_db(self):
        import app.layers.database.python.database.db_main as db_main

        input = {
            'appId': 1,
            'appName': 'ark name',
            'appEmail': 'ark.pes@ark.com'
        }

        result = db_main.translate_to_db(self.app_to_db, input)
        assert result == {
            'db_id': 1,
            'db_name': 'ark name',
            'db_email': 'ark.pes@ark.com'
        }

    def test_trans_db_to_app(self):
        import app.layers.database.python.database.db_main as db_main
        input = {
            'db_id': 1,
            'db_name': 'ark name',
            'db_email': 'ark.pes@ark.com'
        }
        result = db_main.translate_to_app(self.app_to_db, input)
        assert result == {
            'appId': 1,
            'appName': 'ark name',
            'appEmail': 'ark.pes@ark.com'
        }