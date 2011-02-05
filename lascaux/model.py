# -*- coding: utf-8 -*-

if __name__ == "__main__": import sys; sys.path.append('.')

import os.path
import glob

from instlatte.lib.sentient import Sentient

import lascaux
from lascaux.lib.instlatte_setup import new_manager


m = new_manager()
for key in m.config['subsystems'].keys():
    if key != "plugin":
        del m.config['subsystems'][key]
m.setup()
m.execute('find_plugins')
models = list()
for plugin in m.get_subsystem('plugin').get_plugins():
    path = os.path.join(plugin.config['package_dir'], 'model')
    if os.path.isdir(path):
        dotpath = Sentient().get_dotpath(path)
        module = __import__(dotpath)
        for frag in dotpath.split('.')[1:]:
            module = getattr(module, frag)
        for sym in dir(module):
            sym = getattr(module, sym)
            if hasattr(sym, '__export_to_model__') and sym.__export_to_model__:
                models.append(sym)
for model in models:
    if hasattr(model, '__export_to_model_as__'):
        globals()[model.__export_to_model_as__] = model
    else:
        globals()[model.__name__] = model
