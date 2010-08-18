import os.path
import glob

from lascaux.util import parse_config, SUPPORTED_CONFIG_EXTENSIONS
from lascaux import logger
logger = logger(__name__)

import instlatte


class PluginSubSystem(instlatte.SubSystem):
    def discover_plugins(self):
        for source in self.config["sources"]:
            source = os.path.abspath(source)
            for plugin_dir in [d for d in
                               glob.glob(os.path.join(source, "*"))
                               if os.path.isdir(d)]:
                plugin_name = os.path.basename(plugin_dir)
                for ext in SUPPORTED_CONFIG_EXTENSIONS:
                    config_filename = plugin_name+ext
                    if os.path.isfile(os.path.join(plugin_dir,
                                                   config_filename)):
                        logger.info(
                            "Found plugin: `%s` using %s" \
                            % (plugin_name, os.path.join(plugin_dir,
                                                         config_filename)))
                        self.plugins[plugin_name] = {
                            "name": plugin_name,
                            "config_filename": os.path.join(plugin_dir,
                                                            config_filename),
                            "path": plugin_dir}

    def load_plugin(self, Plugin):
        config = parse_config(Plugin["config_filename"])
        entry = Plugin["name"]+"_controller.py"
        module = self.import_file(os.path.join(Plugin["path"], entry))
        class_ = Plugin["name"].title()+"Controller"
        class_ = getattr(module, class_)
        class_.config = config
        Plugin["__class__"] = class_
        logger.info("Loaded plugin: `%s`" % Plugin["name"])
