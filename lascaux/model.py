import os.path
import glob

from storm.locals import create_database, Store

from libel import sl
from lascaux import SObject, config
import instlatte

from lascaux.model_setup import model_modules, model_classes


__db__ = create_database("%s://%s:%s@%s%s/%s" %
                     (config["database"]["interface"],
                      config["database"]["username"],
                      config["database"]["password"],
                      config["database"]["host"],
                      config["database"]["port"] and \
                      ":%s" % config["database"]["port"] or "",
                      config["database"]["database"]))


def create_store():
    return Store(__db__)


# Default store for interactive testing.
# Never --dude, seriously!- never use this for actual development.
db = create_store()


for module in model_modules:
    if "setup" in dir(module):
        module.setup()

for model in model_classes:
    globals()[model] = model_classes[model]
