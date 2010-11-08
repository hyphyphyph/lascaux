import os.path
import glob

from libel import sl

import lascaux
from lascaux.util import parse_config, SUPPORTED_CONFIG_EXTENSIONS
from lascaux.hook import Hook
from lascaux.sys import logger

import instlatte


logger = logger(__name__)


class HookSubsystem(instlatte.Subsystem):

    def _get_hook_sources(self):
        sources = list()
        # TODO: I'd like MetaSubsystem to has a __getattr__ type override
        #       that will echo through to the instance if appropriate.
        for plugin in self.manager.get_subsystem('plugin').instance.get_plugins():
            sources.append(plugin.package_dir)
        for app in lascaux.app_packages:
            sources.append(os.path.dirname(os.path.abspath(app.__file__)))
        sources.append(lascaux.__lib_path__)
        return [os.path.join(s, 'hooks') for s in sources]

    def init(self, log_callback=None):
        # Hooks come from plugins so we need the plugin subsystem
        # to be initialized first.
        if not self.manager.is_subsystem_loaded('plugin'):
            return False
        if log_callback:
            log_callback()
        return self.discover_plugins()

    def discover_plugins(self):
        for source in self._get_hook_sources():
            for h in [h for h in glob.glob(os.path.join(source, '*.py'))
                      if not os.path.basename(h).startswith('_')]:
                name = os.path.basename(os.path.splitext(h)[0])
                p = self.new_plugin(
                    name=name,
                    package_dir=os.path.dirname(h),
                    entry_module=name)
                self.add_plugin(p)
                logger.info(u"discovered hook '%s'" % name)
        return True

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
