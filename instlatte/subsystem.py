import weakref

from libel import SelectionList, sl

from instlatte.object import Object


class SubSystem(Object):

    manager = None
    meta = None
    config = None
    plugins = SelectionList([])

    def __init__(self, Manager, Meta, Init=True):
        self.manager = weakref.proxy(Manager)
        self.import_file = self.manager.import_file
        self.meta = Meta
        self.name = Meta["__config__"]["name"]
        self.config = self.manager.config.has_key(self.name) and \
                      self.manager.config[self.name] or {}
        self.plugins = SelectionList([])
        if Init in (False, True):
            self.init(Init)

    def init(self, Init=True):
        self.discover_plugins()
        if Init:
            self.load_plugins()

    def discover_plugins(self):
        self._discover_plugins()
        for plugin in self.plugins:
            plugin["subsystem"] = self.name
            plugin["loaded"] = plugin.get("loaded") or False

    def _discover_plugins(self):
        pass

    def get_plugin(self, Name):
        results = self.plugins.select("name", sl.EQUALS(Name))
        if not len(results):
            return False
        return results[0]

    def load_plugins(self):
        for plugin in self.plugins:
            if "enabled" not in self.config or \
               (plugin["name"] not in self.config["enabled"] or \
                self.config["enabled"][plugin["name"]]):
                self.load_plugin(plugin)

    def load_plugin(self, Plugin):
        if isinstance(Plugin, basestring):
            Plugin = self.get_plugin(Plugin)
        if self._load_plugin(Plugin) in (True, None):
            Plugin["loaded"] = True

    def _load_plugin(self, Plugin):
        pass

    def execute(self, Plugin, Command, Data={}):
        pass
