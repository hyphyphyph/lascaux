import os
import os.path
import logging


if not os.path.isdir("tmp"):
    os.mkdir("tmp")
logging.basicConfig(filename="tmp/log.txt", level=logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)


def logger(Name):
    logger = logging.getLogger(Name)
    logger.addHandler(stream_handler)
    return logger
