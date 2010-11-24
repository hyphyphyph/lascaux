from storm.locals import create_database, Store

from lascaux.sys import config
from lascaux.lib.model_setup import setup


for model in setup(__name__):
    globals()[model.__name__] = model


__db__ = create_database("%s://%s:%s@%s%s/%s" %
                         (config["database"]["interface"],
                          config["database"]["username"],
                          config["database"]["password"],
                          config["database"]["host"],
                          config["database"]["port"] and \
                          ":%s" % config["database"]["port"] or "",
                          config["database"]["database"]))
store = Store(__db__)
