import os.path
import glob

from instlatte import SubSystem


class Import(SubSystem):

    def _discover_plugins(self):
        for source in self.config["sources"]:
            for file in [f for f in glob.glob(os.path.join(source, "*.py")) \
                         if not os.path.basename(f).startswith("__")]:
                name = os.path.basename(os.path.splitext(file)[0])
                self.plugins.append({"name": name, "__entry__": file})

    def _load_plugin(self, Plugin):
        Plugin["__module__"] = self.import_file(Plugin["__entry__"])
        return True
