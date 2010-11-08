import os.path
import glob

import instlatte

from lascaux.util import parse_config
from lascaux.sys import logger
import lascaux


logger = logger(__name__)


class PluginSubsystem(instlatte.Subsystem):

    def discover_plugins(self):
        for app in lascaux.app_packages:
            path = os.path.join(os.path.dirname(app.__file__),
                                'plugins', '*', '*.json')
        for config_file in glob.glob(path):
            name = os.path.splitext(os.path.basename(config_file))[0]
            p = self.new_plugin(
                name=name,
                package_dir=os.path.dirname(config_file),
                entry_module='%s_controller' % name)
            logger.info(u"%s: discovered plugin '%s'" % (self.meta.name, p.name))
            self.add_plugin(p)

    def init_plugin(self, plugin):
        try:
            parse_config(os.path.join(plugin.package_dir, '%s.json' % plugin.name))
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
