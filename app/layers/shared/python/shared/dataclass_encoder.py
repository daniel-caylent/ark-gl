"""Module that contains util methods for dataclasses encoding"""

import dataclasses


def encode(obj):
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)

    if type(obj) == list:
        for idx in range(len(obj)):
            if dataclasses.is_dataclass(obj[idx]):
                obj[idx] = dataclasses.asdict(obj[idx])
    return obj
