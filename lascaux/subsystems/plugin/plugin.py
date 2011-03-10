# -*- coding: utf-8 -*-

import glob
import os.path

import instlatte
from instlatte.lib import Sentient

from lascaux import config
from lascaux.system.util import parse_config
from lascaux.system.logger import logger
from lascaux.plugin import Plugin


logger = logger(__name__)


class PluginSubsystem(instlatte.Subsystem, Sentient):

    plugins = list()

    def setup(self):
        self.plugins = list()

    def exec_find_plugins(self, app=None):
        self.find_plugins(app)

    def exec_load_plugins(self, app=None):
        self.find_plugins(app)
        self.load_controller_modules(app)
    exec_pre_app_init = exec_load_plugins

    def exec_get_static_dir_mappings(self, mappings):
        static_dir_mappings = self.manager.get_subsystem('server').config['static_dir_mappings']
        for plugin in self.get_plugins():
            def append_mappings(relative, absolute):
                mappings.append([os.path.join(plugin.name, relative), 
                                 os.path.join(plugin.config['package_dir'], absolute)])
                mappings.append([os.path.join(plugin.app_package, plugin.name, relative), 
                                 os.path.join(plugin.config['package_dir'], absolute)])
            for relative in static_dir_mappings:
                append_mappings(relative, static_dir_mappings[relative])
            if 'static_dir_mappings' in plugin.config:
                for relative in plugin.config['static_dir_mappings']:
                    append_mappings(relative, plugin.config['static_dir_mappings'][relative])

    def get_plugins(self):
        return self.plugins

    def find_plugins(self, app=None):
        for app_package in config['app_packages']:
            package_dir = config[app_package]['package_dir']
            for plugin in glob.glob(os.path.join(package_dir, 'plugins', '*')):
                if not os.path.isdir(plugin):
                    continue
                plugin_name = os.path.basename(plugin)
                if not plugin_name in config[app_package]['plugins']:
                    continue
                plugin_config = config[app_package]['plugins'][plugin_name]
                plugin_config['package_dir'] = plugin
                plugin_config['routes'] = parse_config(os.path.join(plugin, plugin_config['routing']))
                if app:
                    self.plugins.append(Plugin(app=app.get_root(), 
                                               name=plugin_name,
                                               app_package=app_package,
                                               config=plugin_config))
                else:
                    self.plugins.append(Plugin(name=plugin_name, 
                                               app_package=app_package,
                                               config=plugin_config))
                logger.info("Found plugin `%s` in '%s'" % (plugin_name, plugin))
        return self.plugins

    def load_controller_modules(self, app=None):
        for plugin in self.plugins:
            for route in plugin.config['routes'].values():
                dotpath = self.get_dotpath(os.path.join(plugin.config['package_dir'], 
                                           route['controller'].split(':')[0]))
                module = __import__(dotpath)
                for sym in dotpath.split('.')[1:]:
                    module = getattr(module, sym)
                class_ = getattr(module, route['controller'].split(':')[1])
                class_.plugin = plugin
                plugin.controllers[route['controller']] = class_
                logger.info("Loaded plugin module for `%s` from '%s'" % (route['controller'], os.path.abspath(module.__file__)))
