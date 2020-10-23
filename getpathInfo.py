import os


def get_path():
    path = os.path.split(os.path.realpath(__file__))[0]
    return path
