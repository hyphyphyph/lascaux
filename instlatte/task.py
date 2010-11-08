# -*- coding: utf-8 -*-

from instlatte import logger


logger = logger(__name__)


class Task(object):

    command = None
    args = dict()
    _selection = list()
    _sel_subsystems = None
    _sel_plugins = None
    _manager = None

    def __init__(self, subsystem=None, subsystems=list(),
                 plugin=None, plugins=list(), manager=None):
        if subsystem:
            self._sel_subsystems = list(subsystem)
        else:
            self._sel_subsystems = subsystems or None
        if plugin:
            self._sel_plugins = list(plugin)
        else:
            self._sel_plugins = plugins or None
        self._manager = manager

    def _get_subsystem(self, subsystem):
        if self._manager:
            return self._manager.get_subsystem(subsystem)
        if self._sel_subsystems:
            for subsystem_ in self._sel_subsystems:
                if not isinstance(subsystem_, basestring) and \
                   subsystem_.name == "subsystem":
                    return subsystem_
        return False

    def _get_plugins_by_name(self, name):
        plugins = list()
        for subsystem in self._manager.get_enabled_subsystems_list():
            for plugin in subsystem.get_enabled_plugins_list():
                if plugin.name == name:
                    plugins.append(plugin)
        return plugins

    def _apply_filter(self, manager):
        plugins = list()
        plugin_names = set()
        final_plugins = set()
        if self._sel_subsystems is not None:
            for subsystem in self._sel_subsystems:
                if isinstance(subsystem, basestring):
                    subsystem = self._get_subsystem(subsystem)
                    if not subsystem:
                        raise ValueError(
             u"Subsystem '%s' can't be found within the available subsystems.")
                map(plugins.append, subsystem.get_enabled_plugins_list())
                map(plugin_names.add, subsystem.get_enabled_plugin_names_list())
        else:
            for subsystem in self._manager.get_enabled_subsystems_list():
                map(plugins.append, subsystem.get_enabled_plugins_list())
                map(plugin_names.add, subsystem.get_enabled_plugin_names_list())
        if self._sel_plugins is not None:
            for plugin in self._sel_plugins:
                if isinstance(plugin, basestring):
                    plugins_ = self._get_plugins_by_name(plugin)
                    map(plugins.append, plugins_)
                    plugin_names.add(plugin)
                else:
                    plugins.append(plugin)
                    plugin_names.add(plugin.name)
        for plugin in plugins:
            if plugin.name in plugin_names:
                final_plugins.add(plugin)
        self._selection = list(final_plugins)

    def execute(self, command, args=dict()):
        logger.info(u"executing %s task" % command)
        task = args or dict()
        self._apply_filter(self._manager)
        subsystems = dict()
        for plugin in self._selection:
            if plugin.subsystem.name not in subsystems:
                subsystems[plugin.subsystem.name] = plugin.subsystem
        returns = list()
        for subsystem in subsystems.values():
            logger.info(u"asking subsystem %s to execute %s" %
                        (subsystem.name, command))
            return_ = subsystem.execute_task(command=command, args=args, task=self)
            if return_:
                returns += return_
        return returns
