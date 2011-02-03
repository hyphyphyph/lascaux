import os.path

try:
    import json
except:
    import simplejson

CONFIG_EXTENSIONS = ["%sjson" % os.path.extsep]


def parse_config(config):
    if os.path.isfile(config):
        file = open(config, "r+")
        config = file.read()
        file.close()
        return json.loads(config.decode())
    else:
        return dict()
