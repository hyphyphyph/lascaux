import os
import os.path


def mkdir(directory):
    directory = os.path.abspath(directory)
    path = os.path.join("/")
    for fragment in directory.split("/"):
        path = os.path.join(path, fragment)
        if not os.path.isdir(path):
            os.mkdir(path)
