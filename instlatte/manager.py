import os.path
import glob
try:
    import json
except:
    import simplejson as json

from libel import SelectionList, sl

from instlatte.object import Object
from instlatte import subsystem
from instlatte import logger


logger = logger(__name__)


class Manager(Object):

    root_path = None
    config = None
    _subsystem_sources = []
    subsystems = SelectionList([])

    def __init__(self, RootPath, Config={}, Init=False):
        self._subsystem_sources = []
        self.subsystems = SelectionList([])

        self.root_path = RootPath
        self.config = Config
        if Init:
            self.init()

    def init(self):
        self.discover_subsystems()
        self.load_subsystems()

    def get_root_path(self):
        return self.root_path

    def add_subsystem_source(self, Source):
        source = os.path.abspath(Source)
        if source not in self._subsystem_sources:
            logger.info("Added subsystem source: %s" % Source)
            self._subsystem_sources.append(source)

    def discover_subsystems(self):
        for source in [source for source in self._subsystem_sources \
                       +[os.path.join(self.get_lib_path(), "subsystems")]]:
            for config_file in glob.glob(os.path.join(source, "*.json")):
                file = open(config_file, 'r')
                config = json.loads(file.read())
                file.close()
                if self.config and \
                   (config["name"] not in self.config or \
                   ("disabled" in self.config[config["name"]] and \
                    self.config[config["name"]]["disabled"] == True)):
                    logger.debug("Ignoring subsystem: %s with %s" %
                                 (config["name"], config_file))
                else:
                    config["__config_file__"] = config_file
                    self.subsystems.append({"__config__": config,
                                            "name": config["name"],
                                            "tags": config.get("tags") or [],
                                            "loaded": False})
                    logger.debug("Found subsystem: %s with %s" %
                                 (config["name"], config_file))

    def select(self, Key, Selector):
        return self.subsystems.select(Key, Selector)

    def get_subsystem(self, SubSystem):
        results = self.subsystems.select("name", sl.EQUALS(SubSystem))
        if not len(results):
            return False
        return results[0]

    def load_subsystems(self, Init=True):
        for subsytem in self.subsystems:
            if self.load_subsystem(subsytem, Init):
                logger.info("Loaded subsytem: %s" % subsytem["name"])
            else:
                logger.warning("Failed to load subsytem: %s" % \
                    subsytem["name"])

    def load_subsystem(self, SubSystem, Init=True):
        if isinstance(SubSystem, basestring):
            SubSystem = self.get_subsystem(SubSystem)
        config = SubSystem["__config__"]
        path = os.path.join(os.path.dirname(config["__config_file__"]),
                            *(config["package"].split(".")))
        entry = "%s_entry" % config["name"]
        entry = self.import_file(os.path.join(path, entry))
        for symbol in dir(entry):
            symbol = getattr(entry, symbol)
            if type(symbol) == type(self.__class__):
                if issubclass(symbol, subsystem.SubSystem) and \
                   subsystem.SubSystem in symbol.__bases__:
                    SubSystem["__instance__"] = symbol(self, SubSystem, Init)
                    SubSystem["loaded"] = True
                    return True
        return False

    def import_file(self, File):
        dot_path = self.determine_dot_path(File)
        module = __import__(dot_path)
        for symbol in dot_path.split(".")[1:]:
            module = getattr(module, symbol)
        logger.debug("Imported a module from %s" % File)
        return module

    def select(self, Key, Selector):
        plugins = SelectionList([])
        for subsystem in self.subsystems:
            for plugin in subsystem["__instance__"].plugins:
                plugins.append(plugin)
        return plugins.select(Key, Selector)

    def execute(self, Selection, Command, Data={}):
        returns = {}
        for plugin in Selection:
            subsystem = self.get_subsystem(plugin["subsystem"])
            subsystem = subsystem["__instance__"]
            returns[plugin["name"]] = subsystem.execute(plugin, Command, Data)
        return returns
