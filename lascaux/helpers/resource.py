import os.path

from libel import sl

from lascaux import SObject, Controller
from lascaux.app import get_manager


def get_resource(resource, plugin=None):
    if issubclass(plugin.__class__, Controller) and \
       Controller in plugin.__class__.__bases__:
        plugin = plugin.name
    m = get_manager(init=True)
    extension = os.path.splitext(resource)[1]
    dirs = []
    if plugin:
        s = m.select("subsystem", sl.EQUALS("lascaux_plugin"))
        s = s.select("name", sl.EQUALS(plugin))
        m.execute(s, "get_static_dirs", dirs)
        for dir in dirs:
            if os.path.isfile(os.path.join(dir[1], resource)):
                resource = os.path.join(dir[0], resource)
                break
    if extension == ".js":
        return u'<script src="/%s" type="text/javascript"></script>' % resource
    elif extension == ".css":
        return u"%s%s />" % (u'<link rel="stylesheet" type="text/css" href="/',
                             resource)
    return u""