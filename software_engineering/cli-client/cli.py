import click
import json
import os
import requests as r
from threading import Thread
from config import ELECTRA_API_ADDRESS, APIKEY_FILE, APIKEY_HEADER_NAME, API_CERT_LOC
import utils
from utils import get_apikey, something_went_wrong, MutuallyExclusiveOption, waiting

@click.group()
def cli():
    pass

@cli.command('HealthCheck')
def HealthCheck():
    res = r.get(ELECTRA_API_ADDRESS + '/HealthCheck', verify=API_CERT_LOC)
    if not something_went_wrong(res):
        click.secho('OK', fg='green')

@cli.command('Reset')
def Reset():
    res = r.post(ELECTRA_API_ADDRESS + '/Reset', verify=API_CERT_LOC)
    if not something_went_wrong(res):
        click.secho('OK', fg='green')

@cli.command('Login')
@click.option('--username', required=True, prompt=True)
@click.option('--passw', required=True, prompt=True, hide_input=True)
def Login(username, passw):

    if os.path.isfile(APIKEY_FILE):
        click.secho('Please logout first', fg='red', err=True)
        exit(1)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'username': username,
        'password': passw
    }

    res = r.post(ELECTRA_API_ADDRESS + '/Login', headers=headers, data=data, verify=API_CERT_LOC)

    if not something_went_wrong(res):

        json_data = json.loads(res.text.strip())
        with open(APIKEY_FILE, 'w') as f:
            f.write(json_data['token'] + '\n')

        click.secho('Login successful. ', fg='green', nl=False)
        click.echo('Welcome to ', nl=False)
        click.secho('electra', bold=True, fg='blue', nl=False)
        click.echo(f', {username}')

@cli.command('Logout')
@click.option('--apikey', type=str, default=None)
def Logout(apikey):
    headers = { APIKEY_HEADER_NAME: get_apikey(apikey) }
    res = r.post(ELECTRA_API_ADDRESS + '/Logout', headers=headers, verify=API_CERT_LOC)

    # if token has expired or the user was deleted, log out anyway
    if 'Token has expired' in res.text or 'that no longer exists' in res.text or not something_went_wrong(res):
        os.remove(APIKEY_FILE)
        click.secho('OK', fg='green')

@cli.command('Account')
@click.option('--apikey', type=str, default=None)
def Account(apikey):
    headers = { APIKEY_HEADER_NAME: get_apikey(apikey) }
    res = r.get(ELECTRA_API_ADDRESS + '/Account', headers=headers, verify=API_CERT_LOC)
    if not something_went_wrong(res):
        json_data = json.loads(res.text.strip())
        click.echo('Account info for user ', nl=False)
        click.secho(json_data['username'], bold=True, nl=False)
        click.echo(':')
        for k, v in json_data.items():
            click.echo(f'{k}: {v}')

@cli.command('ActualTotalLoad')
@click.option('--area', type=str, required=True)
@click.option('--timeres', type=str, required=True)
@click.option('--date', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['month', 'year'])
@click.option('--month', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['date', 'year'])
@click.option('--year', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['month', 'date'])
@click.option('--format', type=str)
@click.option('--apikey', type=str, default=None)
def ActualTotalLoad(area, timeres, date, month, year, format, apikey):

    headers = { APIKEY_HEADER_NAME: get_apikey(apikey) }

    if date is None and month is None and year is None:
        click.secho('date, month or year must be provided', fg='red', err=True)
        exit(1)

    time_option = ('date', date) if date is not None else ('month', month) if month is not None else ('year', year)

    res = r.get(
        ELECTRA_API_ADDRESS + '/ActualTotalLoad/'
                            + area + '/' + timeres + '/' + time_option[0] + '/' + time_option[1]
                            + ('?format=' + format if format is not None else ''),
        headers=headers, verify=API_CERT_LOC
    )

    if not something_went_wrong(res):
        click.echo(res.text.strip())

@cli.command('AggregatedGenerationPerType')
@click.option('--area', type=str, required=True)
@click.option('--timeres', type=str, required=True)
@click.option('--date', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['month', 'year'])
@click.option('--month', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['date', 'year'])
@click.option('--year', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['month', 'date'])
@click.option('--productiontype', type=str, required=True, prompt=True)
@click.option('--format', type=str)
@click.option('--apikey', type=str, default=None)
def AggregatedGenerationPerType(area, timeres, productiontype, date, month, year, format, apikey):

    headers = { APIKEY_HEADER_NAME: get_apikey(apikey) }

    if date is None and month is None and year is None:
        click.secho('date, month or year must be provided', fg='red', err=True)
        exit(1)

    time_option = ('date', date) if date is not None else ('month', month) if month is not None else ('year', year)

    res = r.get(
        ELECTRA_API_ADDRESS + '/AggregatedGenerationPerType/'
                            + area + '/' + productiontype + '/' + timeres + '/' + time_option[0] + '/' + time_option[1]
                            + ('?format=' + format if format is not None else ''),
        headers=headers, verify=API_CERT_LOC
    )

    if not something_went_wrong(res):
        click.echo(res.text.strip())

@cli.command('DayAheadTotalLoadForecast')
@click.option('--area', type=str, required=True)
@click.option('--timeres', type=str, required=True)
@click.option('--date', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['month', 'year'])
@click.option('--month', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['date', 'year'])
@click.option('--year', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['month', 'date'])
@click.option('--format', type=str)
@click.option('--apikey', type=str, default=None)
def DayAheadTotalLoadForecast(area, timeres, date, month, year, format, apikey):

    headers = { APIKEY_HEADER_NAME: get_apikey(apikey) }

    if date is None and month is None and year is None:
        click.secho('date, month or year must be provided', fg='red', err=True)
        exit(1)

    time_option = ('date', date) if date is not None else ('month', month) if month is not None else ('year', year)
    
    res = r.get(
        ELECTRA_API_ADDRESS + '/DayAheadTotalLoadForecast/'
                            + area + '/' + timeres + '/' + time_option[0] + '/' + time_option[1]
                            + ('?format=' + format if format is not None else ''),
        headers=headers, verify=API_CERT_LOC
    )

    if not something_went_wrong(res):
        click.echo(res.text.strip())

@cli.command('ActualvsForecast')
@click.option('--area', type=str, required=True)
@click.option('--timeres', type=str, required=True)
@click.option('--date', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['month', 'year'])
@click.option('--month', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['date', 'year'])
@click.option('--year', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['month', 'date'])
@click.option('--format', type=str)
@click.option('--apikey', type=str, default=None)
def ActualvsForecast(area, timeres, date, month, year, format, apikey):

    headers = { APIKEY_HEADER_NAME: get_apikey(apikey) }

    if date is None and month is None and year is None:
        click.secho('date, month or year must be provided', fg='red', err=True)
        exit(1)

    time_option = ('date', date) if date is not None else ('month', month) if month is not None else ('year', year)

    res = r.get(
        ELECTRA_API_ADDRESS + '/ActualvsForecast/'
                            + area + '/' + timeres + '/' + time_option[0] + '/' + time_option[1]
                            + ('?format=' + format if format is not None else ''),
        headers=headers, verify=API_CERT_LOC
    )

    if not something_went_wrong(res):
        click.echo(res.text.strip())

@cli.command('Admin')
@click.option('--newuser', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['moduser', 'userstatus', 'newdata', 'deluser'])
@click.option('--moduser', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['userstatus', 'newdata', 'newuser', 'deluser'])
@click.option('--deluser', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['userstatus', 'newdata', 'newuser', 'moduser'])
@click.option('--userstatus', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['newuser', 'moduser', 'newdata', 'deluser'])
@click.option('--newdata', type=str, default=None, cls=MutuallyExclusiveOption, mutually_exclusive=['moduser', 'newuser', 'userstatus', 'deluser'])
@click.option('--passw', type=str, default=None)
@click.option('--email', type=str, default=None)
@click.option('--quota', type=str, default=None)
@click.option('--admin', type=bool, default=False)
@click.option('--source', type=click.Path(exists=True), default=None)
@click.option('--apikey', type=str, default=None)
def Admin(newuser, moduser, deluser, userstatus, newdata, passw, email, quota, admin, source, apikey):

    headers = { APIKEY_HEADER_NAME: get_apikey(apikey) }

    if newuser is None and newdata is None and userstatus is None and moduser is None and deluser is None:
        click.secho('No admin action was chosen', fg='red', err=True)
        exit(1)

    if newuser is not None and (passw is None or email is None):
        click.secho('For a new user, a password (--passw) and an email (--email) must be provided', fg='red', err=True)
        exit(1)

    if moduser is not None and (passw is None and email is None and quota is None):
        click.secho('To modify a user, please provide at least one of the following:', fg='red', err=True)
        click.secho('A new password (--passw)', fg='red', err=True)
        click.secho('A new email (--email)', fg='red', err=True)
        click.secho('New quota (--quota)', fg='red', err=True)
        exit(1)

    if newdata is not None and source is None:
        click.secho('CSV file not provided (--source)', fg='red', err=True)
        exit(1)

    data = {
        'username' : newuser,
        'password' : passw,
        'email' : email,
        'is_admin' : admin
    }
    if quota is not None:
        data['quota'] = quota
  
    if newuser is not None:

        res = r.post(ELECTRA_API_ADDRESS + '/Admin/users', headers=headers, data=data, verify=API_CERT_LOC)

        if not something_went_wrong(res):
            click.echo('The new user ', nl=False)
            click.secho(newuser, bold=True, nl=False)
            click.echo(' has been ', nl= False)
            click.secho('successfully ', fg='green', nl=False)
            click.echo('added')

    elif moduser is not None:

        del data['username']
        if passw is None:
            del data['password']
        if email is None:
            del data['email']

        res = r.put(ELECTRA_API_ADDRESS + '/Admin/users/' + moduser, headers=headers, data=data, verify=API_CERT_LOC)

        if not something_went_wrong(res):
            json_data = json.loads(res.text.strip())['updated fields']
            click.secho('Successfully', fg='green', nl=False)
            click.echo(' modified info of user ', nl=False)
            click.secho(moduser, bold=True)
            click.echo(' as follows:')
            for k, v in json_data.items():
                click.echo(f'{k}: {v}')

    elif deluser is not None:

        click.echo('You are about to delete user ', nl=False)
        click.secho(deluser, bold=True, nl=False)
        click.echo('. This action is ', nl=False)
        click.secho('non reversible', bold=True, fg='red', blink=True, nl=False)
        click.echo('.')

        if click.confirm('Are you sure you want to continue?'):

            res = r.delete(ELECTRA_API_ADDRESS + '/Admin/users/' + deluser, headers=headers, verify=API_CERT_LOC)

            if not something_went_wrong(res):
                click.secho('OK', fg='green')

        else:
            click.echo('Aborted.')

    elif userstatus is not None:

        res = r.get(ELECTRA_API_ADDRESS + '/Admin/users/' + userstatus, headers=headers, verify=API_CERT_LOC)

        if not something_went_wrong(res):
            json_data = json.loads(res.text.strip())
            click.echo('Info regarding user ', nl=False)
            click.secho(userstatus, bold=True, nl=False)
            click.echo(':')
            for k, v in json_data.items():
                click.echo(f'{k}: {v}')

    else: # newdata

        with open(source, 'r') as f:
            try:
                utils.request_done = False
                animation = Thread(target=waiting, args=('Importing CSV to database, please wait...',))
                animation.start()
                res = r.post(ELECTRA_API_ADDRESS + '/Admin/' + newdata, headers=headers, files=dict(file=f), verify=API_CERT_LOC)

            except:
                res = None

            finally:
                utils.request_done = True
                animation.join()

        if not something_went_wrong(res):
            json_data = json.loads(res.text.strip())
            click.secho('Successfully', fg='green', nl=False)
            click.echo(' uploaded data in table ', nl=False)
            click.secho(newdata, bold=True, nl=False)
            click.echo(':')
            for k, v in json_data.items():
                click.echo(f'{k}\t{v}')

@cli.command('Contact')
def Contact():

    res = r.get(ELECTRA_API_ADDRESS + '/Contact', verify=API_CERT_LOC)

    if not something_went_wrong(res):
        emails = json.loads(res.text.strip())['admin emails']
        click.echo('Administrator(s) emails:')
        for i, email in enumerate(emails, 1):
            click.echo(f'{i}.\t{email}')

@cli.command('Billing')
@click.option('--number', type=str, required=True, prompt=True)
@click.option('--month', type=int, required=True, prompt=True)
@click.option('--year', type=int, required=True, prompt=True)
@click.option('--cvc', type=int, required=True, prompt=True)
@click.option('--holder', type=str, required=True, prompt=True)
@click.option('--plan', type=str, required=True, prompt=True)
@click.option('--apikey', type=str, default=None)
def Billing(number, month, year, cvc, holder, plan, apikey):

    headers = { APIKEY_HEADER_NAME: get_apikey(apikey) }

    data = {
        'number' : number,
        'month' : month,
        'year' : year,
        'cvc' : cvc,
        'holder' : holder,
        'plan' : plan
    }

    res = r.post(ELECTRA_API_ADDRESS + '/Billing', data=data, headers=headers, verify=API_CERT_LOC)

    if not something_went_wrong(res):
        json_data = json.loads(res.text.strip())
        click.echo('Billing query completed', nl=False)
        click.secho(' successfully', fg='green', nl=False)
        click.echo('. Billing details:')
        for k, v in json_data.items():
            click.echo(f'{k}: {v}')

@cli.command('BillingPlans')
def BillingPlans():
    res = r.get(ELECTRA_API_ADDRESS + '/BillingPlans', verify=API_CERT_LOC)
    if not something_went_wrong(res):
        billing_plan_list = json.loads(res.text.strip())
        click.echo('There are ', nl=False)
        click.secho(f'{len(billing_plan_list)}', bold=True, nl=False)
        click.echo(' billing plans available:')
        for i, billing_plan in enumerate(billing_plan_list, 1):
            click.echo(f'{i}.')
            for k, v in billing_plan.items():
                click.echo(f'\t{k}: {v}')
