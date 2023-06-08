"""Module that contains util methods for dataclasses errors"""

def dataclass_error_to_str(error):
    remove_str = "__init__() got an "
    error_str = str(error).replace(remove_str, "")

    return error_str[0].upper() + error_str[1:]
