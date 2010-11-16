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

    def task___load_enabled_plugins__(self):
        for plugin in self.meta.get_enabled_plugins_list():
            self._load_plugin(plugin)
            logger.info("loaded plugin '%s'" % plugin.name)

    def _load_plugin(self, plugin):
        dot_path = self.determine_dot_path(os.path.join(plugin.package_dir,
                                                        plugin.entry_module))
        module = __import__(dot_path)
        for fragment in dot_path.split('.')[1:]:
            module = getattr(module, fragment)
        for symbol in dir(module):
            symbol = getattr(module, symbol)
            if type(symbol) == type(Hook) and \
               Hook in symbol.__bases__:
                plugin.class_ = symbol
                return True
        return False

    def task_exec_hook(self, hook, app, argc, argv):
        returns = list()
        for plugin in self.meta.get_enabled_plugins_list():
            if hasattr(plugin.class_, u'hook_%s' % hook):
                instance = plugin.class_(app)
                returns.append(getattr(
                    instance, u'hook_%s' % hook)(*argc, **argv))
        return returns
