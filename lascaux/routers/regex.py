# -*- coding: utf-8 -*-

import re

from lascaux.router import Router
from lascaux.execpath import Execpath


class RegexRouter(Router):

    def find_execpath(self, reqres):
        plugins = self.app.manager.get_subsystem('plugin').get_plugins()
        for plugin in plugins:
            for route in plugin.config['routes']:
                exec_path = self.check_match(reqres, route, plugin)
                if exec_path:
                    return exec_path
        return None

    def check_match(self, reqres, route, plugin):
        regex = plugin.config['routes'][route]['regex']
        match = re.match(regex, reqres.uri)
        if match:
            return Execpath(reqres, plugin, route, 
                            plugin.controllers[plugin.config['routes'][route]['controller']],
                            match.groupdict())
        return False
