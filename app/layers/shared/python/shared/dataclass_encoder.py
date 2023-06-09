"""Module that contains util methods for dataclasses encoding"""

import dataclasses


def encode(obj):
    """Convert dataclass objects to dicts"""
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)

    if isinstance(obj, list):
        for idx, _ in enumerate(obj):
            if dataclasses.is_dataclass(obj[idx]):
                obj[idx] = dataclasses.asdict(obj[idx])
    return obj
