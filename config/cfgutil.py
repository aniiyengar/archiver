
import json

class ConfigObject():
    """
    Turns dicts into objects.
    """

    def __init__(self, d=dict()):
        self.__dict__.update(d)


def get_config_object(cfg_dict):
    cfg_str = json.dumps(cfg_dict)
    return json.loads(cfg_str, object_hook=ConfigObject)
