# -*- coding: utf-8 -*-

import os.path
import glob

from instlatte.lib import Sentient

import lascaux
from lascaux.system.logger import logger
from lascaux.server import Server 

import instlatte


logger = logger(__name__)


class ServerSubsystem(instlatte.Subsystem, Sentient):

    servers = list()

    def setup(self):
        self.config.setdefault('sources', list())
        default_source = os.path.abspath(os.path.join(os.path.dirname(lascaux.__file__), 'servers'))
        if default_source not in self.config['sources']:
            self.config['sources'].insert(0, default_source)
        self.servers = list()

    def exec_load_servers(self, app=None):
        self.find_and_load_servers(app)
    exec_pre_app_init = exec_load_servers

    def exec_start_servers(self, app=None):
        for server in self.servers:
            server.start()
    exec_app_start = exec_start_servers

    def find_and_load_servers(self, app=None):
        for source in self.config['sources']:
            for server in filter(lambda f: not os.path.basename(f).startswith('_'),
                                           glob.glob(os.path.join(source, '*%spy' % os.path.extsep))):
                if os.path.isdir(server):
                    continue
                server_name = os.path.basename(os.path.splitext(server)[0])
                if server_name not in self.config['servers'] or not self.config['servers'][server_name]['enabled']:
                    continue
                self._load_server(server, app)

    def _load_server(self, server, app=None):
        server_name = os.path.basename(os.path.splitext(server)[0])
        dotpath = self.get_dotpath(server)
        module = __import__(dotpath)
        for sym in dotpath.split('.')[1:]:
            module = getattr(module, sym)
        for sym in dir(module):
            sym = getattr(module, sym)
            if type(sym) == type(object) and Server in sym.__bases__:
                self.servers.append(sym(app=app, config=self.config['servers'][server_name]))
