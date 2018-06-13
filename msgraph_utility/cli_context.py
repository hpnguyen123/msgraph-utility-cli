import os
import click
import pickle


class Context(object):
    """ Context object for CLI
    """
    def __init__(self):
        self.verbose = False
        self.tokens = None
        self.home = os.getcwd()
        self.config = os.path.expanduser('~/.li_msgraph')

        if self.config and os.path.isfile(self.config):
            self._deserialize()

    def _serialize(self):
        pickle.dump(self, open(self.config, "wb"))

    def _deserialize(self):
        data = pickle.load(open(self.config, "rb"))
        self.__dict__.update(data.__dict__)

    def save(self, tokens):
        if tokens != self.tokens:
            self.tokens = tokens
            self._serialize()

        return tokens


pass_context = click.make_pass_decorator(Context, ensure=True)
