import os.path

try:
    import json
except:
    import simplejson


SUPPORTED_CONFIG_EXTENSIONS = [".json"]


def parse_config(Config):
    if os.path.isfile(Config):
        file = open(Config, "r+")
        Config = file.read()
        file.close()
    return json.loads(Config.decode())
