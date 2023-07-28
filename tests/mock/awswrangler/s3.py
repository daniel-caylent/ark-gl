import json

def read_json(path=None, lines=None):
    return DataframeMocked()
    
class DataframeMocked:
    def to_json(self, orient=None):
        return json.dumps([
            {
                "transactionInfo": {
                    "statements": [
                        {"statement": "INSERT INTO"}
                    ]
                },
                "revisions": [
                    {"data": "data"}
                ]
            }
        ])