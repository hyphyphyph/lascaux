import os.path
import glob

from storm.locals import create_database, Store

from libel import sl
from lascaux import SObject, config
import instlatte


db = create_database("%s://%s:%s@%s%s/%s" % 
                     (config["database"]["interface"],
                      config["database"]["username"],
                      config["database"]["password"],
                      config["database"]["host"],
                      config["database"]["port"] and \
                      ":%s" % config["database"]["port"] or "",
                      config["database"]["database"]))


def create_store():
    return Store(db)


__manager__ = instlatte.Manager(SObject().get_lib_path(),
                                {"lascaux_plugin":
                                 config["subsystems"]["lascaux_plugin"]}, False)
__manager__.add_subsystem_source(os.path.join("lascaux", "subsystems"))
__manager__.discover_subsystems()
__manager__.load_subsystems(Init=False)
plugins = __manager__.execute(__manager__.select("subsystem", 
                                                 sl.EQUALS("lascaux_plugin")), 
                              "list")
for plugin in plugins.values():
    path = plugin[0]["__path__"]
    if os.path.isdir(os.path.join(path, "model")):
        for file in glob.glob(os.path.join(path, "model", "*.py")):
            dot_path = SObject().determine_dot_path(file)
            module = __import__(dot_path)
            for fragment in dot_path.split(".")[1:]:
                module = getattr(module, fragment)
            for symbol in dir(module):
                obj = getattr(module, symbol)
                if hasattr(obj, "__export_to_model__") and \
                   obj.__export_to_model__:
                    globals()[symbol] = obj