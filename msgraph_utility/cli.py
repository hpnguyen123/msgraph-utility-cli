import os
import click
import json
from . import auth
from .cli_context import pass_context
from .helpers import extract_path, get_stdin
from msgraph_utility import api as api_util


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--verbose', '-v', is_flag=True, help='Print output verbose')
@pass_context
def cli(ctx, verbose):
    """ CLI Utility to interact with MSGraph API
    """
    ctx.verbose = verbose


@cli.command()
@pass_context
@click.argument('client-id')
def init(ctx, client_id):
    """ Invoke authentication workflow
    """
    tokens = auth.acquire_token_with_device_code(client_id, auto=False)
    ctx.save(tokens=tokens, client_id=client_id)


@cli.command('put-file')
@click.option('--destination', '-d', required=True, help='Destination file on OneDrive')
@click.argument('file-path', required=True)
@pass_context
def put_file(ctx, file_path, destination):
    """ Put content of a file to OneDrive
    """
    tokens = auth.ensure_tokens(ctx.client_id, ctx.tokens)
    ctx.save(tokens=tokens)

    session = auth.get_request_session(tokens)
    with open(file_path, 'r') as file:
        data = file.read()

    _, file_name = extract_path(file_path)
    destination_path, destination_name = extract_path(destination)
    destination_name = destination_name if destination_name else file_name

    response = session.put(auth.api_endpoint(f'me/drive/root:{destination_path}{destination_name}:/content'),
                           headers={'Content-Type': 'text/plain'},
                           data=data)

    if ctx.verbose:
        click.echo(response.text)
    else:
        click.echo(f'response {response.status_code}')


@cli.command('get-file')
@click.argument('file-path', required=True)
@pass_context
def get_file(ctx, file_path):
    """ Get content of a file from OneDrive
    """
    tokens = auth.ensure_tokens(ctx.client_id, ctx.tokens)
    ctx.save(tokens=tokens)
    session = auth.get_request_session(tokens)

    # Calling helper method to get the file
    api_util.get_file(session, file_path)


@cli.command('get-content')
@click.argument('drive-id', required=False)
@click.argument('item-id', required=False)
@pass_context
def get_content(ctx, drive_id, item_id):
    """ Get content of a file from OneDrive given drive_id and item_id
    """
    session = ctx.get_request_session()

    if drive_id and item_id:
        api_util.get_content(session, drive_id, item_id, verbose=ctx.verbose)

    for item in get_stdin():
        api_util.get_content(session, item['drive-id'], item['item-id'], file_name=item.get('file-name'), verbose=ctx.verbose)


@cli.command('get')
@click.argument('api', required=True)
@pass_context
def get_api(ctx, api):
    """ Generic GET api on MSGRAPH
    """
    tokens = auth.ensure_tokens(ctx.client_id, ctx.tokens)
    ctx.save(tokens=tokens)
    session = auth.get_request_session(tokens)
    api_util.get(session, api, verbose=ctx.verbose)


@cli.command('show')
@click.argument('property')
@pass_context
def show(ctx, property):
    """ Show the configuration property
    """
    click.echo(ctx.__dict__[property])


@cli.command('test')
@pass_context
def test(ctx):
    """ Test
    """
    stdin = click.get_text_stream('stdin').read()
    with click.progressbar(length=1, label='Unzipping archive') as count:
        click.echo(f'{count} {stdin}')


def main():
    cli()


if __name__ == "__main__":
    cli()
