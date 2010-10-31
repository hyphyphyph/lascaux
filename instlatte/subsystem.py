import os.path
import weakref

from libel import SelectionList, sl

from instlatte.sobject import SObject
from instlatte import logger


logger = logger(__name__)


class MetaPlugin(object):

    name = None
    package_dir = None
    entry_module = u"__init__"
    config = dict()

    subsystem = None

    def set_subsystem(self, subsystem):
        """
        subsystem should be the MetaSubsystem
        """
        self.subsystem = subsystem

    def init(self):
        if self.subsystem.is_plugin_enabled(self):
            self.subsystem.load_plugin(self)


class MetaSubsystem(SObject):

    package_dir = None
    name = None
    is_loaded = False
    config = dict()
    instance = None

    def __init__(self, package_dir, config=dict()):
        self.package_dir = package_dir
        self.name = os.path.basename(package_dir)
        self.config = config or dict()

        if "enabled" not in self.config:
            self.config["enabled"] = dict()

    def set_instance(self, instance):
        self.instance = instance

    def _get_class_name(self, name):
        return u"%sSubsystem" % name.replace("_", "").title()

    def _get_module_name(self, name):
        return u"%s_entry" % name

    def load(self, manager=None):
        dot_path = self.determine_dot_path(self.package_dir)
        dot_path = u"%s.%s" % (dot_path, self._get_module_name(self.name))
        module = __import__(dot_path)
        for fragment in dot_path.split(".")[1:]:
            module = getattr(module, fragment)
        class_ = self._get_class_name(self.name)
        try:
            class_ = getattr(module, class_)
            instance = class_(meta=self, manager=manager)
            self.set_instance(instance)
            logger.info(u"loaded subsystem '%s'", self.name)
            self.loaded = True
            self.instance.discover_plugins()
            return True
        except AttributeError as e:
            logger.error(u"%s'%s'  %s'%s'" % (u"could not load subsystem ",
                                              self.name,
                                              u"no class named ", class_))
            raise e
        return False

    def init_plugins(self):
        status = list()
        for plugin in self.instance.plugins:
            if self.instance.is_plugin_enabled(plugin):
                if self.instance.init_plugin(plugin):
                    status.append(True)
                    logger.info(u"initialized plugin '%s'" % plugin.name)
                else:
                    status.append(False)
                    logger.error(u"failed to initialize plugin '%s'" %
                                 plugin.name)
        return status

    def list_enabled_plugin_names(self):
        return [p.name for p in self.instance.plugins
                if self.instance.is_plugin_enabled(p)]

    def list_enabled_plugins(self):
        return [p for p in self.instance.plugins
                if self.instance.is_plugin_enabled(p)]

    def execute_task(self, command, args=dict(), task=None):
        if hasattr(self.instance, u"task_%s" % command):
            return getattr(self.instance, u"task_%s" % command)(**args)
        else:
            return self.instance.execute_task(command, args, task)
        

class Subsystem(SObject):

    manager = None
    meta = None
    plugins = SelectionList(list())

    def __init__(self, meta, manager=None):
        if manager:
            self.manager = weakref.proxy(manager)
        self.meta = weakref.proxy(meta)
        self.plugins = SelectionList(list())


    def discover_plugins(self):
        """
        Populates self.plugins with a MetaPlugin instances
        for the available/found plugins.
        """
        pass

    def is_plugin_enabled(self, plugin):
        if not isinstance(plugin, basestring):
            plugin = plugin.name
        return plugin in self.meta.config["enabled"] and \
               self.meta.config["enabled"][plugin] or False

    def enable_plugin(self, plugin):
        if not isinstance(plugin, basestring):
            plugin = plugin.name
        self.meta.config["enabled"][plugin] = True
        logger.info(u"enabled '%s'" % plugin)

    def disable_plugin(self, plugin):
        if not isinstance(plugin, basestring):
            plugin = plugin.name
        self.meta.config["enabled"][plugin] = False
        logger.info(u"disabled '%s'" % plugin)

    def new_plugin(self, name, package_dir, entry_module=u"__init__"):
        p = MetaPlugin()
        p.set_subsystem(self.meta)
        p.name = name
        p.package_dir = package_dir
        p.entry_module = entry_module
        return p

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
        if not plugin.name in self.meta.config["enabled"]:
            self.enable_plugin(plugin)
        else:
            if self.meta.config["enabled"][plugin.name]:
                logger.info(u"'%s' already enabled. leaving alone" %
                            plugin.name)
            else:
                logger.info(u"'%s' forcefully disabled" % plugin.name)

    def init_plugin(self):
        """
        Should do the very minimal amount required to initialize a plugin.
        Generally, this would be loding config files and the like.
        Most of the time, this shouldn't actually involve loading any
        plugin code, as that should be left to a task.
        Returns True for success, False for failure.
        """
        return True
    
    def execute_task(self, command, args=dict(), task=None):
        pass
