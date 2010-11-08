import os.path
import glob

from libel import sl

import lascaux
from lascaux.util import parse_config, SUPPORTED_CONFIG_EXTENSIONS
from lascaux.hook import Hook
from lascaux.sys import logger
logger = logger(__name__)

import instlatte


class HookSubsystem(instlatte.Subsystem):

    def get_sources(self):
        sources = []
        obj = lascaux.SObject()
        sources.append(os.path.join(obj.get_lib_path(), "hooks"))
        sources.append(os.path.join(self.get_exec_path(), "hooks"))
        plugins = self.manager.select("subsystem", sl.EQUALS("lascaux_plugin"))
        for plugin in plugins:
            path = os.path.join(plugin["__path__"], "hooks")
            if os.path.isdir(path) and \
               os.path.isfile(os.path.join(path, "__init__.py")):
                sources.append(path)
        return sources

    def _discover_plugins(self, init_hooks=False):
        # TODO: This is seriously ugly...  Get the frick rid of this.
        """
        --- You need to have a way to get execute commands on the subsystem
            itself, not just on plugins of the subsystem.
        --- It should be noted also, subsystems should load entirely, then move
            onto the next, that way a subsystem should be able to access
            another subsystem in the loading process.
            --- This will require the use of prereq parsing.
        """
        if not init_hooks:
            self.plugins.append({"name": "__lascaux_hook_dummy__"})
        else:
            for source in self.get_sources():
                for file in filter(lambda f: \
                                   not os.path.basename(f).startswith("_"),
                                   glob.glob(os.path.join(source, "*.py"))):
                    module = self.import_file(file)
                    for symbol in dir(module):
                        class_ = getattr(module, symbol)
                        if type(class_) is type(self.__class__) and \
                           issubclass(class_, Hook) and \
                           Hook in class_.__bases__:
                            responds_to = []
                            for responder in dir(class_):
                                if responder.startswith("hook_"):
                                    responds_to.append(responder[5:])
                            config = {
                                "name": class_.__name__,
                                "subsystem": "lascaux_hook",
                                "__path__": source,
                                "__file__": os.path.join(source, file),
                                "__class__": class_,
                                "responds_to": responds_to}
                            class_.path = config["__path__"]
                            self.plugins.append(config)

    def _load_plugin(self, Plugin, init_hooks=False):
        if init_hooks:
            pass

    def exec_hook(self, plugin, data):
        if data["hook"] in plugin["responds_to"]:
            controller = "controller_" in data["data"] and \
                    data["data"]["controller_"] or None
            request = "request_" in data["data"] and \
                    data["data"]["request_"] or None
            instance = plugin["__class__"](controller=controller,
                                           request=request)
            data_ = {}
            for key in data["data"]:
                if key not in ("controller_", "request_"):
                    data_[key] = data["data"][key]
            return getattr(instance, "hook_%s" % data["hook"])(**data_)
        return None

    def execute(self, Plugin, Command, Data={}):
        if Command == "_discover_plugins":
            self._discover_plugins(True)
        if Plugin["name"] == "__lascaux_hook_dummy__":
            return None
        if Command == "exec_hook":
            return self.exec_hook(Plugin, Data)
