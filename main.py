import os.path
try:
    import json
except:
    import simplejson as json

import lascaux.sys


app_config_file = os.path.abspath("config.json")
app_config_file = open(app_config_file, "r")
app_config = json.loads(app_config_file.read())
app_config_file.close()

env = lascaux.sys.Environment()
for app in app_config["app_packages"]:
    package = __import__(app)
    env.add_app_package(package)
env.init()

app = lascaux.sys.App(env)
