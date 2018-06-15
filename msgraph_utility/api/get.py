import os
import click
from msgraph_utility import auth
from msgraph_utility.helpers import extract_path

def get_file(session, file_path=None, verbose=False):
    """ Get content of a file from OneDrive
    """
    file_dir, file_name = extract_path(file_path)
    api = auth.api_endpoint(f'me/drive/root:{file_dir}{file_name}:/content')
    process_response(session.get(api), api, file_name=file_name, verbose=verbose)


def get_content(session, drive_id, item_id, file_name=None, verbose=False):
    """ Get the content of the drive-id and item-id
    """
    api = auth.api_endpoint(f'/drives/{drive_id}/items/{item_id}/content')
    process_response(session.get(api), api, file_name=file_name, verbose=verbose)


def get(session, api, file_name=None, verbose=False):
    """ Generic GET api on MSGRAPH
    """
    api = auth.api_endpoint(api)
    process_response(session.get(api), api, file_name=file_name, verbose=verbose)


def process_response(response, api, file_name=None, verbose=False):
    """ Process the reponse by saving to file or print to output stream
    """
    if file_name:
        with open(file_name, 'w') as file:
            file.write(response.text)

    if verbose:
        click.echo(response.text)
    else:
        click.echo(f'({response.status_code}) {api}')
