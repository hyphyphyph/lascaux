import os.path
import glob

from libel import sl
from lascaux import SObject, config
import instlatte


__manager__ = instlatte.Manager(SObject().get_lib_path(),
                                {"lascaux_plugin":
                                 config["subsystems"]["lascaux_plugin"]},
                                False)
__manager__.add_subsystem_source(os.path.join("lascaux", "subsystems"))
__manager__.discover_subsystems()
__manager__.load_subsystems(Init=False)
__plugins__ = __manager__.execute(__manager__.select("subsystem",
                                                 sl.EQUALS("lascaux_plugin")),
                                  "list")

model_modules = []
model_classes = {}

for plugin in __plugins__.values()[0]:
    path = plugin["__path__"]
    if os.path.isdir(os.path.join(path, "model")):
        for file in glob.glob(os.path.join(path, "model", "*.py")):
            dot_path = SObject().determine_dot_path(file)
            module = __import__(dot_path)
            for fragment in dot_path.split(".")[1:]:
                module = getattr(module, fragment)
            model_modules.append(module)
            for symbol in dir(module):
                class_ = getattr(module, symbol)
                if hasattr(class_, "__export_to_model__") and \
                   class_.__export_to_model__:
                    model_classes[symbol] = class_
                    globals()[symbol] = class_
