import os
import click
from . import auth
from .cli_context import pass_context
from .helpers import extract_path


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--verbose', '-v', is_flag=True, help='Print output verbose')
@pass_context
def cli(ctx, verbose):
    """ CLI Utility to interact with MSGraph API
    """
    ctx.verbose = verbose


@cli.command()
@pass_context
@click.option('--client-id', required=True, help='Client ID for native application')
def authenticate(ctx, client_id):
    """ Invoke authentication workflow
    """
    tokens = auth.acquire_token_with_device_code(client_id, auto=False)
    ctx.save(tokens=tokens, client_id=client_id)


@cli.command('put-content')
@click.option('--destination', '-d', required=True, help='Destination file on OneDrive')
@click.argument('file-path', required=True)
@pass_context
def put_content(ctx, file_path, destination):
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


@cli.command('get-content')
@click.argument('file-path', required=True)
@pass_context
def get_content(ctx, file_path):
    """ Get content of a file from OneDrive
    """
    tokens = auth.ensure_tokens(ctx.client_id, ctx.tokens)
    ctx.save(tokens=tokens)

    file_dir, file_name = extract_path(file_path)
    session = auth.get_request_session(tokens)
    response = session.get(auth.api_endpoint(f'me/drive/root:{file_dir}{file_name}:/content'))

    with open(file_name, 'w') as file:
        file.write(response.text)

    if ctx.verbose:
        click.echo(response.text)
    else:
        click.echo(f'response {response.status_code}')


@cli.command('show')
@click.argument('property')
@pass_context
def show(ctx, property):
    """ Show the configuration property
    """
    click.echo(ctx.__dict__[property])


def main():
    cli()


if __name__ == "__main__":
    cli()
