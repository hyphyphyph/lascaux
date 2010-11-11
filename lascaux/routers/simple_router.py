import re
from libel import sl

from lascaux.baserouter import BaseRouter


class SimpleRouter(BaseRouter):

    def find_route(self, app, request):
        plugins = app.manager.get_subsystem('plugin')
        plugins = plugins.get_enabled_plugins_list()
        for plugin in plugins:
            routes = plugin.plugin_config.get('routes', dict())
            for route_name in routes:
                route = routes[route_name]['simple']
                regex = self._get_regex(route)
                match = regex.match(request.uri)
                if match:
                    request.exec_plugin = plugin
                    request.exec_route = routes[route_name]
                    args = {}
                    for fragment in route.split("/"):
                        if fragment.startswith("{") and fragment.endswith("}"):
                            name, type = fragment[1:-1].split(":")
                            if type == "#":
                                args[str(name)] = int(match.groups() \
                                                  [len(args)])
                            else:
                                args[name] = unicode(match.groups()[len(args)])
                    request.exec_args = args
                    return True
        return False

    def _get_regex(self, route):
        regex_fragments = [""]
        for fragment in route.split("/"):
            if fragment.startswith("{") and fragment.endswith("}"):
                name, type = fragment[1:-1].split(":")
                if type == "*":
                    regex_fragments.append("([\S]+)")
                elif type == "$":
                    regex_fragments.append("([\W_]+)")
                elif type == "#":
                    regex_fragments.append("([\d]+)")
            else:
                regex_fragments.append(fragment)
        return re.compile("^" + "/".join(regex_fragments) + "[/]?$", re.U)

    def _get_arguments(self, route):
        args = []
        for fragment in route.split("/"):
            if fragment.startswith("{"):
                fragment = fragment.strip("{}")
                args.append(fragment.split(":")[0])
        return args

    def _sub_args(self, route, args):
        fragments = []
        for fragment in route.split("/"):
            if fragment.startswith("{"):
                try:
                    fragment = fragment.strip("{}").split(":")[0]
                    fragments.append(unicode(args[fragment]))
                except:
                    raise ValueError("Required route argument not supplied.")
            else:
                fragments.append(fragment)
        return u"/".join(fragments)

    def get_route(self, request, controller, action, args={}):
        args = args or {}
        plugins = request.app.manager.select("subsystem",
                                             sl.EQUALS("lascaux_plugin"))
        matches = []
        for plugin in plugins:
            plugin_ = plugin["__class__"]
            if controller == plugin_.name:
                for route in plugin_.routes:
                    if action == plugin_.routes[route]["action"]:
                        matches.append(route)
        for match in matches:
            for arg in self._get_arguments(match):
                if arg not in args.keys():
                    continue
            return u"/%s" % self._sub_args(match, args)
        return False
