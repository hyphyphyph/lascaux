import sys
import os
import os.path

import instlatte


class Object:

    __exec_path__ = None
    __lib_path__ = None
    __self_path__ = None

    def get_exec_path(self, Force=False):
        """
        Absolute path of os.getcwd().
        """
        if not self.__exec_path__ or Force:
            self.__exec_path__ = os.path.abspath(os.getcwd())
        return self.__exec_path__

    def get_lib_path(self, Force=False):
        """
        Points to the absolute path of the instlatte library
        """
        if not self.__lib_path__ or Force:
            self.__lib_path__ = os.path.abspath(
                os.path.dirname(instlatte.__file__))
        return self.__lib_path__

    def get_self_path(self, Force=False, Source=True):
        """
        Absolute path for the module of the current class
        (applies to subclasses as well)
        If Source is True, returns the .py, rather than the pyc or pyo
        """
        if not self.__self_path__ or Force:
            if self.__module__ == "__main__":
                self.__self_path__ = os.path.join(os.getcwd(), sys.argv[0])
            else:
                self.__self_path__ = sys.modules[self.__module__].__file__
        if Source:
            if os.path.splitext(self.__self_path__)[1] in (".pyc", ".pyo"):
                return os.path.splitext(self.__self_path__)[0] + ".py"
        return self.__self_path__

    def determine_dot_path(self, File):
        """
        Returns the dot path for importing the module
        contained in a given file.
        """
        file = os.path.splitext(os.path.abspath(File))[0]
        for path in sys.path:
            path = os.path.abspath(path)
            if file.startswith(path):
                relative = file[len(path) + 1:]
        fragments = []
        split = os.path.split(relative)
        while split[1]:
            fragments.append(split[1])
            relative = split[0]
            split = os.path.split(split[0])
        fragments.reverse()
        return ".".join(fragments)
