import sys
import os
import os.path
import gettext


class SentientObject:

    __exec_path__ = None
    __lib_import__ = __import__("libel")
    __lib_path__ = None
    __self_path__ = None

    __i18n_domain__   = None
    __i18n_language__ = "en_US"


    def get_exec_path(self, Force=False):
        """
        Absolute path of os.getcwd().
        """
        if not self.__exec_path__ or Force:
            self.__exec_path__ = os.path.abspath(os.getcwd())
        return self.__exec_path__

    def get_lib_path(self, Force=False):
        """
        Points to the absolute path of the lib_import module/package
        """
        if not self.__lib_path__ or Force:
            self.__lib_path__ = os.path.abspath(
                os.path.dirname(self.__lib_import__.__file__))
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

    def i18n(self, domain="main", language=None):
        """
        Provides module based localization.
        Domain is a path relative to SelfPath that specifies the location
        of the translation catalog. ".." or "../.." or example.
        Language is the language to use.  Really?  Yes.
        """
        source_append = ""
        if domain:
            domain = os.path.basename(domain)
            source_append = os.path.dirname(domain)
        elif self.__i18n_domain__:
            domain = os.path.basename(self.__i18n_domain__)
            source_append = os.path.dirname(self.__i18n_domain__)
        else:
            domain = self.__class__.__name__.lower()
        if not language:
            language = self.__i18n_language__
        sources = [
            os.path.join(self.get_exec_path(), source_append),
            os.path.join(self.get_lib_path(), source_append),
            os.path.join(os.path.dirname(self.get_self_path()), source_append)]
        for i, s in enumerate(sources):
            sources[i] = os.path.abspath(s)
        for i, s in enumerate(sources):
            sources[i] = os.path.join(s, "locale")
        sources_ = []
        for source in sources:
            if source not in sources_:
                sources_.append(source)
        for source in sources:
            if gettext.find(domain, source, [language]):
                return gettext.translation(domain, source, [language]).ugettext
        return gettext.translation(domain, fallback=True).ugettext

    def set_lang(self, language):
        self.__i18n_language__ = language

    def get_lang(self):
        return self.__i18n_language__
