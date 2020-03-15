from flask import Flask, request, render_template, url_for, redirect, flash, make_response
from flask_navigation import Navigation
from config import (
    PREFIX,
    ELECTRA_API_ADDRESS,
    API_CERT_LOC
)
from utils import create_token_header
import requests as r
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'askjfalkfbglhubvfliusdbg'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['STATIC_AUTO_RELOAD'] = True

nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Αρχική σελίδα', 'index'),
    nav.Item('Ο λογαριασμός μου', 'account'),
    nav.Item('Υπηρεσίες χρέωσης', 'billing'),
    nav.Item('Επικοινωνία', 'contact')
])

dataset_dict = {'ActualTotalLoad': 'Actual Total Load', 'AggregatedGenerationPerType': 'Aggregated Generation Per Type', 'DayAheadTotalLoadForecast': 'Day-Ahead Total Load Forecast', 'ActualvsForecast': 'Actual Total Load vs Day-Ahead Total Load Forecast'}
res_dict = {'PT15M': '15 λεπτά', 'PT30M': '30 λεπτά', 'PT60M': '60 λεπτά'}
prodtypes = ['Fossil Gas', 'Hydro Run-of-river and poundage', 'Hydro Pumped Storage', 'Hydro Water Reservoir', 'Fossil Hard coal', 'Nuclear', 'Fossil Brown coal/Lignite', 'Fossil Oil', 'Fossil Oil shale', 'Biomass', 'Fossil Peat', 'Wind Onshore', 'Other', 'Wind Offshore', 'Fossil Coal-derived gas', 'Waste', 'Solar', 'Geothermal', 'Other renewable', 'Marine', 'AC Link', 'Transformer', 'DC Link', 'Substation', 'AllTypes']
names = {'dataset_dict': dataset_dict, 'res_dict': res_dict, 'prodtypes':prodtypes}

@app.route(PREFIX, methods=['GET'])
def index():
    username = request.cookies.get('username')
    return render_template('index.html', username=username, names=names)

@app.route(PREFIX + 'contact/', methods=['GET'])
def contact():
    api_resp = r.get(ELECTRA_API_ADDRESS + '/Contact', verify=API_CERT_LOC)
    admin_emails = api_resp.json()['admin emails']
    return render_template('contact.html', admin_emails=admin_emails, names=names)

@app.route(PREFIX + 'data/', methods=['GET', 'POST'])
def data():

    header = create_token_header(request.cookies.get('token'))

    if header is None:
        flash('Δεν είστε συνδεδεμένος/-η.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('index.html', search=True, names=names)

    if request.method == 'POST':
        dataset = '/' + request.form.get('dataset')
        areaname = '/' + request.form.get('areaname')
        prodtype = '/' + request.form.get('prodtype') if dataset == '/AggregatedGenerationPerType' else ''
        alltypes = True if prodtype == '/AllTypes' else False
        res = '/' + request.form.get('resolution')
        datetype = '/' + request.form.get('datetype')

        url = ELECTRA_API_ADDRESS + dataset + areaname + prodtype + res + datetype + '/' + request.form.get('year')

        if datetype in ['/date', '/month']:
            url += '-' + request.form.get('month')
        if datetype in ['/date']:
            url += '-' + request.form.get('day')

        response = r.get(url, headers=header, verify=API_CERT_LOC)
        
        if response.status_code == 200:
            data = json.loads(response.text.strip())
            return render_template('results.html', data=data, dataset=dataset[1:], dataset_descr=dataset_dict[dataset[1:]], res=res[1:], datetype=datetype[1:], alltypes=alltypes, prodtypes=prodtypes[:-1], names=names)
        elif response.status_code == 400: # bad request
            flash('Εισάγατε λάθος κάποια στοιχεία. Προσπαθήστε ξανά.', 'danger')
            return redirect(url_for('data'))
        elif response.status_code == 402: # out of quota
            flash('Έχετε χρησιμοποιήσει όλα τα επιτρεπόμενα αιτήματά σας για το τρέχον λεπτό. Παρακαλούμε, προσπαθήστε ξανά αργότερα.', 'danger')
            return redirect(url_for('index'))
        elif response.status_code == 403: # no data
            return render_template('nodata.html', names=names)
        else:
            flash('Κάποιο απρόσμενο σφάλμα συνέβη. Παρακαλούμε, προσπαθήστε ξανά αργότερα.', 'danger')
            return redirect(url_for('index'))

### user access endpoints ###
@app.route(PREFIX + '/login', methods=['GET', 'POST'])
def login():
    username = request.cookies.get('username')
    if username:
        return render_template('login.html', username=username, names=names)
    # form to login
    if request.method == 'GET':
        return render_template('login.html', names=names)
    # request to login
    if request.method == 'POST':
        username = request.form.get('username')
        data = {
            'username': username,
            'password': request.form.get('password')
        }
        api_resp = r.post(ELECTRA_API_ADDRESS + '/Login', data=data, verify=API_CERT_LOC)
        if api_resp.status_code == 200:
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('username', username, secure=True, httponly=False)
            resp.set_cookie('token', api_resp.json()['token'], secure=True, httponly=True)
            flash('Επιτυχής σύνδεση, καλωσορίσατε στο electra!', 'success')
            return resp
        else:
            flash('Λάθος όνομα χρήστη και/ή κωδικός πρόσβασης. Παρακαλούμε, προσπαθήστε ξανά.', 'danger')
            return make_response(redirect(url_for('login')))

@app.route(PREFIX + '/logout', methods = ['GET'])
def logout():
    header = create_token_header(request.cookies.get('token'))
    if header is not None:
        api_resp = r.post(ELECTRA_API_ADDRESS + '/Logout', headers=header, verify=API_CERT_LOC)
    else:
        flash('Δεν είστε συνδεδεμένος/-η.', 'danger')
        return redirect(url_for('login'))
    resp = make_response(redirect(url_for('index')))
    if api_resp.status_code == 200 or 'expired' in api_resp.text or 'revoked' in api_resp.text:
        resp.delete_cookie('username')
        resp.delete_cookie('token')
    else:
        flash('Κάποιο απρόσμενο σφάλμα συνέβη. Παρακαλούμε, προσπαθήστε ξανά αργότερα.', 'danger')
    return resp

@app.route(PREFIX + 'account/')
def account():
    header = create_token_header(request.cookies.get('token'))

    if header is not None:
        api_resp = r.get(ELECTRA_API_ADDRESS + '/Account', headers=header, verify=API_CERT_LOC)
    else:
        flash('Δεν είστε συνδεδεμένος/-η.', 'danger')
        return redirect(url_for('login'))

    account = api_resp.json()
    del account['password hash']
    return render_template('account.html', account=account, names=names)

@app.route(PREFIX + 'billing/', methods=['GET', 'POST'])
def billing():
    header = create_token_header(request.cookies.get('token'))

    # firstly, see if the user has an active billing plan
    if header is not None:
        api_resp = r.get(ELECTRA_API_ADDRESS + '/Account', headers=header, verify=API_CERT_LOC)
    else:
        flash('Δεν είστε συνδεδεμένος/-η.', 'danger')
        return redirect(url_for('login'))

    user_account_info = api_resp.json()
    if user_account_info['billing plan'] != 'F(ree)':
        flash(f'Έχετε ήδη μία ενεργή χρέωση τύπου {user_account_info["billing plan"]}', 'danger')
        flash('Εάν επιθυμείτε κάποια αλλαγή, παρακαλούμε επικοινωνείστε με κάποιον διαχειριστή.', 'info')
        return redirect(url_for('index'))

    if request.method == 'GET':
        api_resp = r.get(ELECTRA_API_ADDRESS + '/BillingPlans', verify=API_CERT_LOC)
        if api_resp.status_code == 200:
            billing_plan_list = [plan for plan in json.loads(api_resp.text.strip()) if plan['plan'] != 'F(ree)' and plan['plan'] != 'DEV']
            return render_template('billing.html', plans=billing_plan_list[::-1], names=names)
        else:
            flash('Κάποιο απρόσμενο σφάλμα συνέβη. Παρακαλούμε, προσπαθήστε ξανά αργότερα.', 'danger')
            return redirect(url_for('index'))

    if request.method == 'POST':

        fields = ['number', 'year', 'month', 'cvc', 'holder', 'plan']

        data = { field : request.form.get(field) for field in fields }
        data['plan'] = data['plan'].split()[0].replace('+', 'p')
        print(data)
        api_resp = r.post(ELECTRA_API_ADDRESS + '/Billing', headers=header, data=data, verify=API_CERT_LOC)
        if api_resp.status_code == 200:
            flash(f'Συγχαρητήρια! Μόλις αποκτήσατε το πλάνο {data["plan"].replace("p", "+")}! Σας ευχαριστούμε για την υποστήριξη!', 'success')
        else:
            flash('Κάποιο απρόσμενο σφάλμα συνέβη. Παρακαλούμε, προσπαθήστε ξανά αργότερα.', 'danger')
        return redirect(url_for('index'))
