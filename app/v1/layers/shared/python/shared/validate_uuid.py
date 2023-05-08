import uuid

def validate_uuid(uuid_: str, throw=False):
    try:
        uuid.UUID(uuid_)
    except Exception:
        if throw is not False:
            raise Exception('Invalid UUID.')

        return False

    return uuid_