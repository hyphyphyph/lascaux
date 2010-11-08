if __name__ == "__main__": import sys; sys.path.append(".")
import os.path
import glob

from instlatte import Manager
from lascaux.config import config
import lascaux


def get_subsystem_sources():
    subsystems = set()
    for dir_ in [os.path.join(lascaux.__lib_path__, 'subsystems')]:
        for f in [f for f in glob.glob(os.path.join(dir_, "*", "*.py"))
                  if not os.path.basename(f).startswith("_") and
                  not os.path.basename(os.path.dirname(f)).startswith("_")]:
            subsystems.add(os.path.dirname(f))
    return list(subsystems)


def new_manager():
    m = Manager(config.get('instlatte', dict()))
    map(m.add_subsystem, get_subsystem_sources())
    m.init()
    return m
