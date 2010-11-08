import os.path

from lascaux.util import parse_config, SUPPORTED_CONFIG_EXTENSIONS


__lib_path__ = os.path.abspath(os.path.dirname(__file__))
__exec_path__ = os.path.abspath('.')

__config__ = parse_config(os.path.join(__exec_path__, "config.json"))
app_packages = set()
for app in  __config__.get('app_packages', list()):
    package = __import__(app)
    app_packages.add(package)
app_packages = list(app_packages)
