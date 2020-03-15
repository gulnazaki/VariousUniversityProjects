import click
from requests.status_codes import codes
from config import APIKEY_FILE
import itertools
import time
import sys

def get_apikey(apikey_from_command_line):

    if apikey_from_command_line is not None:
        return apikey_from_command_line

    try:
        with open(APIKEY_FILE, 'r') as f:
            apikey = f.read().strip()
    except:
        click.secho('API key not found. ', fg='red', nl=False, err=True)
        click.echo('Are you logged in?', err=True)
        exit(1)

    return apikey

def something_went_wrong(response):
    if (response is None or response.status_code != codes['OK']):
        click.secho('[!] electra API ERROR [!]', blink=True, bold=True, fg='red', err=True)
        if response is not None:
            click.echo(response.text.strip(), err=True)
        else:
            click.echo('Your CSV file is invalid OR the dataset you provided does not exist OR you are not logged in as admin.')
        exit(42)
    return False

class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = help + (
                ' NOTE: This argument is mutually exclusive with '
                ' arguments: [' + ex_str + '].'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )

# animation while waiting for csv upload
request_done = False

def waiting(message):

    global request_done

    bar = [
        ' [=     ]',
        ' [ =    ]',
        ' [  =   ]',
        ' [   =  ]',
        ' [    = ]',
        ' [     =]',
        ' [    = ]',
        ' [   =  ]',
        ' [  =   ]',
        ' [ =    ]'
    ]

    for c in itertools.cycle(bar):
        if request_done:
            break
        sys.stdout.write(f'\r{message}' + c)
        sys.stdout.flush()
        time.sleep(0.2)
    click.echo(f'\r{message} ', nl=False)
    click.secho('OK' + ' ' * (len(bar[0]) - 1), fg='green')
