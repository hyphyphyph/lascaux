if __name__ == "__main__": import sys; sys.path.append(".")
import os.path
import glob

from instlatte import Manager
import lascaux


def get_subsystems_list():
    subsystems = set()
    for dir_ in [os.path.join(lascaux.__lib_path__, 'subsystems')]:
        for f in [f for f in glob.glob(os.path.join(dir_, "*", "*.py"))
                  if not os.path.basename(f).startswith("_") and
                  not os.path.basename(os.path.dirname(f)).startswith("_")]:
            subsystems.add(os.path.dirname(f))
    return list(subsystems)


def new_plugin_manager():
    m = Manager(lascaux.__config__)
    p = os.path.join(lascaux.__lib_path__, 'subsystems', 'plugin')
    if os.path.isdir(p):
        m.add_subsystem(p)
    m.init()
    return m
