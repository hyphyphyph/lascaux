import re
from libel import sl

from lascaux.baserouter import BaseRouter

class SimpleRouter(BaseRouter):
    def find_route(self, App, Request):
        plugins = App.manager.select("subsystem", sl.EQUALS("lascaux_plugin"))
        for plugin in plugins:
            plugin_ = plugin["__class__"]
            for route in plugin_.routes:
                regex = self._get_regex(route)
                match = regex.match(Request.URI)
                if match:
                    Request.exec_plugin = plugin
                    Request.exec_route = plugin_.routes[route]
                    args = {}
                    for fragment in route.split("/"):
                        if fragment.startswith("{") and fragment.endswith("}"):
                            name, type = fragment[1:-1].split(":")
                            if type == "#":
                                args[str(name)] = int(match.groups() \
                                                  [len(args)])
                            else:
                                args[name] = unicode(match.groups()[len(args)])
                    Request.exec_args = args
                    return True
        return False

    def _get_regex(self, Route):
        regex_fragments = [""]
        for fragment in Route.split("/"):
            if fragment.startswith("{") and fragment.endswith("}"):
                name, type = fragment[1:-1].split(":")
                if type == "*":
                    regex_fragments.append("([\S]+")
                elif type == "$":
                    regex_fragments.append("([\W_])+")
                elif type == "#":
                    regex_fragments.append("([\d]+)")
            else:
                regex_fragments.append(fragment)
        return re.compile("/".join(regex_fragments) + "[/]?", re.U)
    
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
                fragment = fragment.strip("{}").split(":")[0]
                fragments.append(unicode(args[fragment]))
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