import os.path
import glob

import lascaux
from lascaux.sys import SObject
from lascaux.lib.instlatte_setup import new_manager


__manager__ = None


def get_manager():
    global __manager__
    if not __manager__:
        __manager__ = new_manager()
    return __manager__


def get_sources(package):
    manager = get_manager()
    if not isinstance(package, basestring):
        package = package.__name__
    app_path = os.path.abspath(os.path.dirname(__import__(package).__file__))
    sources = [os.path.join(app_path, 'model')]
    for p in glob.glob(os.path.join(app_path, 'plugins', '*', '*.json')):
        if p.startswith(app_path) and not \
           os.path.basename(os.path.dirname(p)).startswith('_'):
            sources.append(os.path.join(os.path.dirname(p), 'model'))
    return sources


def get_models(sources):
    modules = list()
    classes = list()
    for source in sources:
        for file in glob.glob(os.path.join(source, '*.py')):
            dot_path = SObject().determine_dot_path(file)
            module = __import__(dot_path)
            for symbol in dot_path.split('.')[1:]:
                module = getattr(module, symbol)
            modules.append(module)
            for symbol in dir(module):
                class_ = getattr(module, symbol)
                if hasattr(class_, '__export_to_model__'):
                    classes.append(class_)
    return modules, classes


def setup_models(models):
    for module in models[0]:
        if 'setup' in dir(module):
            module.setup()
    return models[1]


def setup(package):
    return setup_models(get_models(get_sources(package)))
