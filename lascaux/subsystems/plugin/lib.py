import os.path
import glob

from lascaux.util import SUPPORTED_CONFIG_EXTENSIONS
import lascaux


def is_plugin_enabled(plugin):
    try:
        enabled = lascaux.__config__['subsystem_config'] \
                                    ['plugin'] \
                                    ['enabled'] \
                                    [plugin]
    except:
        enabled = None
    return enabled or False

def get_plugin_dirs():
    dirs = set()
    sources = [os.path.join(os.path.abspath(os.path.dirname(p.__file__)), 'plugins')
               for p in lascaux.app_packages]
    for s in sources:
        for p in [p for p in glob.glob(os.path.join(s, '*', '*.*')) if
                  os.path.splitext(p)[1] in SUPPORTED_CONFIG_EXTENSIONS and
                  os.path.basename(os.path.dirname(p))[0] not in ('.', '_')]:
            dirs.add(os.path.dirname(p))
    return list(dirs)

def get_plugin_names():
    return map(get_plugin_name, get_plugin_dirs())

def get_plugin_name(plugin):
    return os.path.basename(plugin)
