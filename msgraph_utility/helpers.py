""" General utility methods
"""
import os


def extract_path(path):
    """ Extract the path to path and basename
    """
    dir_name = os.path.dirname(path)
    dir_name = prepend_slash(dir_name)
    dir_name = append_slash(dir_name)
    base_name = os.path.basename(path)

    return (dir_name, base_name)


def prepend_slash(path):
    return path if path.startswith('/') else f'/{path}'


def append_slash(path):
    return path if path.endswith('/') else f'{path}/'
