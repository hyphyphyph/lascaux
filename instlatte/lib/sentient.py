import sys
import os.path


class Sentient(object):

    def get_dotpath(self, file_):
        file_ = os.path.splitext(os.path.abspath(file_))[0]
        for path in sys.path:
            path = os.path.abspath(path)
            if file_.startswith(path):
                relative = file_[len(path) + 1:]
        fragments = []
        split = os.path.split(relative)
        while split[1]:
            fragments.append(split[1])
            relative = split[0]
            split = os.path.split(split[0])
        fragments.reverse()
        return '.'.join(fragments)
