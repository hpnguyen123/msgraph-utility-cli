import os
import click
import pickle
from . import auth


class Context(object):
    """ Context object for CLI
    """
    def __init__(self):
        self.verbose = False
        self.tokens = None
        self.client_id = None
        self.history = []
        self.home = os.getcwd()
        self.config = os.path.expanduser('~/.li_msgraph')

        if self.config and os.path.isfile(self.config):
            self._deserialize()

    def _serialize(self):
        pickle.dump(self, open(self.config, "wb"))

    def _deserialize(self):
        data = pickle.load(open(self.config, "rb"))
        self.__dict__.update(data.__dict__)

    def save(self, tokens=None, client_id=None):
        dirty = False
        if tokens and tokens != self.tokens:
            self.tokens = tokens
            dirty = True

        if client_id and client_id != self.client_id:
            self.client_id = client_id
            dirty = True

        if dirty:
            self._serialize()

    def get_request_session(self):
        """ Gets the current session.  If token expired, refresh token
        """
        tokens = auth.ensure_tokens(self.client_id, self.tokens)
        self.save(tokens=tokens)
        return auth.get_request_session(tokens)


pass_context = click.make_pass_decorator(Context, ensure=True)
