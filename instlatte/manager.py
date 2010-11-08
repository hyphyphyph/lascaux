# -*- coding: utf-8 -*-

import os.path
import glob
try:
    import json
except:
    import simplejson as json

from libel import SelectionList, sl

from instlatte.sobject import SObject
from instlatte import subsystem
from instlatte import logger
from instlatte.task import Task


logger = logger(__name__)


class Manager(SObject):

    subsystems = SelectionList(list())
    config = dict()

    def __init__(self, config=dict()):
        self.subsystems = SelectionList(list())
        self.config = config or {"enabled": dict()}
        if 'enabled' not in self.config:
            self.config['enabled'] = {}

    def add_subsystem(self, package_dir, config=dict()):
        """
        Adds a subsystem to the manager.  Give the absolute directory
        of the Python package containing the subsytem.
        """
        m = subsystem.MetaSubsystem(package_dir=package_dir)
        c = config or self.config.get("subsystem_config", {}).get(m.name, [])
        m.set_config(c)
        self.subsystems.append(m)
        logger.info(u"[+] added subsystem '%s'" % m.name)
        if m.name not in self.config.get("enabled", []):
            self.enable_subsystem(m)
        else:
            if self.config["enabled"][m.name]:
                logger.info(u"'%s' already enabled. Leaving alone." % m.name)
            else:
                logger.info(u"'%s' forcefully disabled." % m.name)

    def init(self):
        self.init_subsystems()
        self.init_subsystem_plugins()

    def init_subsystems(self):
        init_queue = [s.name for s in self.subsystems]
        while init_queue:
            subsystem = self.get_subsystem(init_queue[0])
            if self.is_subsystem_enabled(subsystem):
                init_queue.pop(0)
                def log_callback():
                    logger.info(
                    u"performing subsystem initialization for '%s'..." %
                        subsystem.name)
                if not self.init_subsystem(subsystem, log_callback):
                    init_queue.append(subsystem.name)
                    logger.info(
                    u"postponing subsystem initialization for '%s'" %
                        subsystem.name)
                else:
                    logger.info(u"initialized subsystem '%s'" %
                                subsystem.name)

    def init_subsystem(self, subsystem, log_callback=None):
        """
        Instantiates the subsystem entry into the given MetaSubsystem.
        """
        return subsystem.init(manager=self, log_callback=log_callback)

    def init_subsystem_plugins(self):
        for subsystem in self.subsystems:
            if self.is_subsystem_enabled(subsystem):
                subsystem.init_plugins()

    def is_subsystem_enabled(self, subsystem):
        if not isinstance(subsystem, basestring):
            subsystem = subsystem.name
        return subsystem in self.config["enabled"] and \
               self.config["enabled"][subsystem] or False

    def enable_subsystem(self, subsystem):
        if not isinstance(subsystem, basestring):
            subsystem = subsystem.name
        self.config["enabled"][subsystem] = True
        logger.info(u"enabled subsystem '%s'" % subsystem)

    def disable_subsystem(self, subsystem):
        if not isinstance(subsystem, basestring):
            subsystem = subsystem.name
        self.config["enabled"][subsystem] = False
        logger.info(u"disabled %s" % subsystem)

    def get_enabled_subsystems_list(self):
        return [s for s in self.subsystems
                if self.is_subsystem_enabled(s)]

    def is_subsystem_loaded(self, name):
        for subsystem in self.subsystems:
            if subsystem.name == name:
                return subsystem.is_loaded
        return None

    def get_subsystem(self, name):
        for subsystem in self.subsystems:
            if subsystem.name == name:
                return subsystem
        return False

    def execute(self, command, args=dict(), plugins=list(), subsystems=list()):
        args = args or dict()
        task = Task(plugins=plugins, subsystems=subsystems, manager=self)
        return task.execute(command, args)
