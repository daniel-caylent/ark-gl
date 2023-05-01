import uuid

def validate_uuid(uuid_: str, throw=False):
    if uuid_ is None:
        return None

    try:
        uuid.UUID(uuid_)
    except Exception:
        if throw is not False:
            raise Exception('Invalid UUID.')

        return False

    return uuid_