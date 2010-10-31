import os.path
try:
    import json
except:
    import simplejson as json

import lascaux


app_config_file = os.path.abspath("config.json")
app_config_file = open(app_config_file, "r")
app_config = json.loads(app_config_file.read())
app_config_file.close()

env = lascaux.Environment()
for app in app_config["apps"]:
    package = __import__(app)
    env.add_app_package(package)

app = lascaux.App(env)
