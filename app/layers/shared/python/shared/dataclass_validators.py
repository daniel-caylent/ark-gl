"""Module that contains util methods for dataclasses validations"""

from .validate_uuid import validate_uuid


def check_uuid(uuid, name) -> str:
    """Validate a uuid"""
    if uuid is None:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"Required argument is missing: {name}."
        )

    try:
        validate_uuid(uuid, throw=True)
    except:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"{name} is not a valid UUID."
        )

    return uuid


def validate_bool(bool_, name, strict=False):
    """Validate a boolean exists for this value"""
    if bool_ is None:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"Required argument is missing: {name}."
        )

    if strict:
        if type(bool_) is not bool:
            raise Exception(
                f"{name} is not a boolean."
            )

    try:
        bool_ = bool(bool_)
    except:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"{name} is not a valid boolean."
        )
    return bool_


def validate_str(str_, name, min_len=0, max_len=256, allowed: list = None) -> str:
    """Validate a string exists for this value"""
    if str_ is None:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"Required argument is missing: {name}."
        )

    try:
        str_ = str_.strip()
    except:
        raise Exception(
            f"{name} is invalid."
        )  # pylint: disable=broad-exception-raised,raise-missing-from

    if len(str_) < min_len:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"{name} does not meet min length requirement of {min_len} characters."
        )
    if len(str_) > max_len:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"{name} does not meet max length requirement of {max_len} characters."
        )

    if allowed:
        if str_ not in allowed:
            raise Exception(
                f"{name} is not one of allowed: {str(allowed).strip('[]')}."
            )

    return str_


def validate_int(
    int_, name: str, min: int=None, max: int=None, allowed: list=None
) -> int:
    """Validate an integer exists for this value"""

    if int_ is None:
        raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
            f"Required argument is missing: {name}."
        )

    if "." in str(int_):
        raise Exception(
            f"{name} contains an invalid integer: {int_}"
        )

    try:
        int_ = int(str(int_))
    except:
        raise Exception(
            f"{name} is invalid."
        )  # pylint: disable=broad-exception-raised,raise-missing-from

    if min is not None:
        if int_ < min:
            raise Exception(f"{name} is invalid.")

    if max is not None:
        if int_ > max:
            raise Exception(f"{name} is invalid.")

    if allowed:
        if int_ not in allowed:
            raise Exception(  # pylint: disable=broad-exception-raised,raise-missing-from
                f"{name} must be one of {allowed}."
            )

    return int_
