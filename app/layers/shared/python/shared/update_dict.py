"""Module that defines util methods for dictionary manipulation"""

def update_dict(base_dict: dict, target_dict: dict) -> dict:
    """Updates the values of base_dict from the values of matching keys
    in update_dict
    """
    return_dict = {}
    for key in base_dict.keys():
        return_dict[key] = target_dict[key]

    return return_dict
