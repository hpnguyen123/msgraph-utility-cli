import os
import click
from . import auth
from .cli_context import pass_context


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--verbose', '-v', is_flag=True, help='Print output verbose')
@pass_context
def cli(ctx, verbose):
    """ CLI Utility to interact with MSGraph API
    """
    ctx.verbose = verbose


@cli.command()
@pass_context
def authenticate(ctx):
    """ Invoke authentication workflow
    """
    tokens = auth.acquire_token_with_device_code(auto=False)
    ctx.save(tokens=tokens)


@cli.command('put-content')
@click.option('--destination', '-d', required=True, help='Destination file on OneDrive')
@click.argument('file', required=True)
@pass_context
def put_content(ctx, file, destination):
    """ Put content of a file to OneDrive
    """
    tokens = auth.ensure_tokens(ctx.tokens)
    ctx.save(tokens=tokens)

    session = auth.get_request_session(tokens)

    with open(file, 'r') as file:
        data = file.read()

    response = session.put(auth.api_endpoint(f'me/drive/root:{destination}:/content'),
                           headers={'Content-Type': 'text/plain'},
                           data=data)

    if ctx.verbose:
        print(response.text)
    else:
        print(f'response {response.status_code}')


@cli.command('get-content')
@click.argument('file', required=True)
@pass_context
def get_content(ctx, file):
    """ Get content of a file from OneDrive
    """
    tokens = auth.ensure_tokens(ctx.tokens)
    ctx.save(tokens=tokens)

    session = auth.get_request_session(tokens)
    response = session.get(auth.api_endpoint(f'me/drive/root:{file}:/content'))

    file_name = os.path.basename(file)

    with open(file_name, 'w') as file:
        file.write(response.text)

    if ctx.verbose:
        print(response.text)
    else:
        print(f'response {response.status_code}')


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
