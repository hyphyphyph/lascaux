import os.path

from crepehat import SObject


class Kitchen(SObject):

    sources = []
    extensions = []

    def __init__(self, sources, extensions=None):
        if not hasattr(sources, "__iter__"):
            sources = [sources]
        self.sources = sources
        if extensions and not hasattr(extensions, "__iter__"):
            extensions = [extensions]
        self.extensions = extensions

    def get(self, path, extensions=None, overridable=True):
        if self.extensions and extensions != False or extensions:
            path = os.path.splitext(path)[0]
        if not hasattr(extensions, "__iter__"):
            extensions = self.extensions
        if not overridable:
            if extensions:
                if os.path.isfile(os.path.join(self.sources[-1],
                                               path+self.extensions[-1])):
                    return os.path.join(self.sources[-1],
                                        path+self.extensions[-1])
            else:
                if os.path.isfile(os.path.join(self.sources[-1],
                                               path)):
                    return os.path.join(self.sources[-1],
                                        path)
            return False
        for source in self.sources:
            j = os.path.join(source, path)
            if extensions:
                for ext in extensions:
                    if os.path.isfile(j+ext):
                        return j+ext
            else:
                if os.path.isfile(j):
                    return j
        return False
