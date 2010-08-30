import os.path
import glob

from lascaux import SObject
from lascaux import logger
logger = logger(__name__)

import instlatte


class ServerSubsystem(instlatte.SubSystem):

    def discover_plugins(self):
        obj = SObject()
        for source in self.config["sources"]+ \
            [os.path.join(obj.get_lib_path(), "servers")]:
            for file in filter(lambda f: \
                not os.path.basename(f).startswith("_") \
                and not os.path.basename(f).startswith("."),
                               glob.glob(os.path.join(source, "*.py"))):
                self.plugins.append({
                    "name": os.path.basename(os.path.splitext(file)[0]),
                    "__file__": file
                })
