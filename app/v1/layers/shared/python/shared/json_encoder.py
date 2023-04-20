import dataclasses, json

class EnhancedJSONEncoder(json.JSONEncoder):
    """
    Allow encoding of dataclass objects to json
    """
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return super().default(obj)
