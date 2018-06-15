""" General utility methods
"""
import os
import click
import json


def extract_path(path):
    """ Extract the path to path and basename
    """
    dir_name = os.path.dirname(path)
    dir_name = prepend_slash(dir_name)
    dir_name = append_slash(dir_name)
    base_name = os.path.basename(path)

    return (dir_name, base_name)


def prepend_slash(path):
    """ Add a slash in front
    """
    return path if path.startswith('/') else f'/{path}'


def append_slash(path):
    """ Add a slash at the end
    """
    return path if path.endswith('/') else f'{path}/'


def get_stdin():
    """ Get std input as a list
    """
    results = []
    raw = click.get_text_stream('stdin').read()
    if raw:
        data = json.loads(raw)
        if isinstance(data, (list, tuple)):
            results.extend(data)
        else:
            results.append(data)

    return results
