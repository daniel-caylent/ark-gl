"""Module that defines util methods for UUID validation"""

import uuid

def validate_uuid(uuid_: str, throw=False):
    """Throw an error or return False if the input is not a UUID"""
    try:
        uuid.UUID(uuid_)
    except Exception as e:
        if throw is not False:
            raise Exception("Invalid UUID.") from e

        return False

    return uuid_
