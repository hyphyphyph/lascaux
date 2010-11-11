import os.path
import glob

import instlatte

from lascaux.subsystems.plugin.lib import get_plugin_dirs, get_plugin_name

from lascaux.util import parse_config
from lascaux.sys import logger


logger = logger(__name__)


class PluginSubsystem(instlatte.Subsystem):

    def discover_plugins(self):
        for dir_ in get_plugin_dirs():
            p = self.new_plugin(
                name=get_plugin_name(dir_),
                package_dir=dir_,
                entry_module='%s_controller' % get_plugin_name(dir_))
            logger.info(u"%s: discovered plugin '%s'" % (self.meta.name, p.name))
            self.add_plugin(p)
        return True

    def init_plugin(self, plugin):
        try:
            config = parse_config(os.path.join(plugin.package_dir,
                                               '%s.json' % plugin.name))
            plugin.plugin_config = config
            return True
        except Exception, e:
            raise e

    def task___load_enabled_plugins__(self):
        for plugin in self.meta.get_enabled_plugins_list():
            self._load_plugin(plugin)
            logger.info("loaded plugin '%s'" % plugin.name)

    def _load_plugin(self, plugin):
        dot_path = self.determine_dot_path(plugin.package_dir)
        dot_path = "%s.%s" % (dot_path, plugin.entry_module)
        module = __import__(dot_path)
        for fragment in dot_path.split('.')[1:]:
            module = getattr(module, fragment)
        class_name = '%sController' % plugin.name.title().replace('_', '')
        class_ = getattr(module, class_name)
        plugin.class_ = class_
        plugin.class_.config = plugin.plugin_config

    def task_get_static_dirs(self, dirs):
        for plugin in self.meta.get_enabled_plugins_list():
            dirs += plugin.class_.get_static_dirs(plugin)
