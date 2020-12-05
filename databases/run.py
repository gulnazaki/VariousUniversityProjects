from flask import Flask, flash, render_template
from flask import redirect, url_for, request, session
import tabulate
import datetime

from module.dbRent import Rent
from module.dbReserve import Reserve
from module.dbQuery import Query
from module.dbCustomer import Customer
from module.dbFleet import Fleet

app = Flask(__name__)
app.secret_key = "*OMADARAVASEIS*"

dbRent = Rent()
dbReserve = Reserve()
dbCustomer = Customer()
dbFleet = Fleet()
Query = Query()

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/rent/')
def ShowRents():
    RentsData = dbRent.ShowRents(None, None)

    return render_template('/rent/show.html', data = RentsData)

@app.route('/rent/add')
def AddRent():
    return render_template('/rent/add.html')

@app.route('/rent/addrent', methods = ['POST'])
def Handler_AddRent():
    if (request.method == 'POST' and request.form['save']):
        if dbRent.AddRent(request.form):
            flash("A new rent has been Added")
        else:  
            flash('Opps! Something wrong happened')

    return redirect(url_for('ShowRents'))

@app.route('/rent/update/<string:licenseplate>/<string:startdate>')
def UpdateRent(licenseplate, startdate):
    Rent = dbRent.ShowRents(licenseplate, startdate)

    if not Rent:
        return redirect(url_for('ShowRents'))
    else:
        return render_template('/rent/update.html', data = Rent)

@app.route('/rent/updaterent', methods = ['POST'])
def Handler_UpdateRent():
    if (request.method == 'POST' and request.form['updaterent']):
    
        if (dbRent.UpdateRent(request.form)):
            flash('Rent has been Updated')
        else:
            flash('Opps! Something wrong happened')

    return redirect(url_for('ShowRents'))

@app.route('/rent/delete/<string:licenseplate>/<string:startdate>')
def DeleteRent(licenseplate, startdate):
    Rent = dbRent.ShowRents(licenseplate, startdate)

    if not Rent:
        return redirect(url_for('ShowRents'))
    else:
        return render_template('/rent/delete.html', data = Rent)

@app.route('/rent/deleterent', methods = ['POST'])
def Handler_DeleteRent():

    if (request.method == 'POST' and request.form['deleterent']):
        if (dbRent.DeleteRent(request.form)):
            flash('Rent has been Deleted')
        else:
            flash('Opps! Something wrong happened')

    return redirect(url_for('ShowRents'))

@app.route('/reserve/')
def ShowReserves():
    ReservesData = dbReserve.ShowReserves(None, None)

    return render_template('/reserve/show.html', data = ReservesData)

@app.route('/reserve/add')
def AddReserve():
    return render_template('/reserve/add.html')

@app.route('/reserve/addrent', methods = ['POST'])
def Handler_AddReserve():
    if (request.method == 'POST' and request.form['save']):
        if dbReserve.AddReserve(request.form):
            flash("A new reserve has been Added")
        else:  
            flash('Opps! Something wrong happened')

    return redirect(url_for('ShowReserves'))

@app.route('/reserve/update/<string:licenseplate>/<string:startdate>')
def UpdateReserve(licenseplate, startdate):
    Reserve = dbReserve.ShowReserves(licenseplate, startdate)

    if not Reserve:
        return redirect(url_for('ShowReserves'))
    else:
        return render_template('/reserve/update.html', data = Reserve)

@app.route('/reserve/updatereserve', methods = ['POST'])
def Handler_UpdateReserve():
    if (request.method == 'POST' and request.form['updatereserve']):
    
        if (dbReserve.UpdateReserve(request.form)):
            flash('Reserve has been Updated')
        else:
            flash('Opps! Something wrong happened')

    return redirect(url_for('ShowReserves'))

@app.route('/reserve/delete/<string:licenseplate>/<string:startdate>')
def DeleteReserve(licenseplate, startdate):
    Reserve = dbReserve.ShowReserves(licenseplate, startdate)

    if not Reserve:
        return redirect(url_for('ShowReserves'))
    else:
        return render_template('/reserve/delete.html', data = Reserve)

@app.route('/reserve/deletereserve', methods = ['POST'])
def Handler_DeleteReserve():
    if (request.method == 'POST' and request.form['deletereserve']):
        if (dbReserve.DeleteReserve(request.form)):
            flash('Reserve has been Deleted')
        else:
            flash('Opps! Something wrong happened')
    return redirect(url_for('ShowReserves'))

@app.route('/customer/')
def ShowCustomers():
    CustomerData = dbCustomer.ShowCustomers(None)

    return render_template('/customer/show.html', data = CustomerData)

@app.route('/customer/add')
def AddCustomer():
    return render_template('/customer/add.html')

@app.route('/customer/addrent', methods = ['POST'])
def Handler_AddCustomer():
    if (request.method == 'POST' and request.form['save']):
        if dbCustomer.AddCustomer(request.form):
            flash("A new customer has been Added")
        else:  
            flash('Opps! Something wrong happened')

    return redirect(url_for('ShowCustomers'))

@app.route('/customer/update/<int:id>/')
def UpdateCustomer(id):
    Customer = dbCustomer.ShowCustomers(id)

    if not Customer:
        return redirect(url_for('ShowCustomers'))
    else:
        session['UpdatedCustomer'] = id
        return render_template('/customer/update.html', data = Customer)

@app.route('/customer/updatecustomer', methods = ['POST'])
def Handler_UpdateCustomer():
    if (request.method == 'POST' and request.form['updatecustomer']):
    
        if (dbCustomer.Hi(request.form, session['UpdatedCustomer'])):
            flash('Customer has been Updated')
        else:
            flash('Opps! Something wrong happened')

        session.pop('UpdatedCustomer', None)

    return redirect(url_for('ShowCustomers'))

@app.route('/customer/delete/<string:id>')
def DeleteCustomer(id):
    Customer = dbCustomer.ShowCustomers(id)

    if not Customer:
        return redirect(url_for('ShowCustomers'))
    else:
        session['DeletedCustomer'] = id
        return render_template('/customer/delete.html', data = Customer)

@app.route('/customer/deletecustomer', methods = ['POST'])
def Handler_DeleteCustomer():
    if (request.method == 'POST' and request.form['deletecustomer']):
        if (dbCustomer.DeleteCustomer(session['DeletedCustomer'])):
            flash('Customer has been Deleted')
        else:
            flash('Opps! Something wrong happened')

        session.pop('DeletedCustomer', None)

    return redirect(url_for('ShowCustomers'))

@app.route('/sql/<int:nquery>')
def Query_Handler(nquery):
    if nquery:
        with open('./queries/{0}.sql'.format(nquery), "r") as f:
            sqlQ = f.read()

            (Res, Des) = Query.ExecQuery(sqlQ)

            if (Res and Des):
                (Header, Rows) = handle_data(Res, Des)
            else:
                Header = ["Empty"]
                Rows = [["No Data"]]

        return render_template('/sql/exec.html', header=Header, data=Rows, query=sqlQ)

@app.route('/tables/<string:table>')
def Table(table):
    with open('./tables/{0}.sql'.format(table), "r") as f:
        sqlQ = f.read()

        (Res, Des) = Query.ExecQuery(sqlQ)

        (Header, Rows) = handle_data(Res, Des)

    return render_template('/tables/index.html', header=Header, data=Rows, title=table)


@app.route('/v')
def View1():
    (Res, Des) = Query.ExecQuery("SELECT * FROM `customersrents`")

    (Header, Rows) = handle_data(Res, Des)
    flash("Not Updateable View")

    return render_template('/view1/show.html', data=Rows)


@app.route('/v2')
def View2():
    Data = dbFleet.Show(None)

    if not Data:
        return render_template('/view2/show.html')
    else:
        return render_template('/view2/show.html', data=Data)

@app.route('/v2/update/<string:plate>')
def ViewUpdate(plate):
    Data = dbFleet.Show(plate)

    if not Data:
        return redirect(url_for('View2'))
    else:
        return render_template('/view2/update.html', data=Data)  

@app.route('/v2/updateview', methods = ['POST'])
def Handle_Update():
    if (request.method == 'POST' and request.form['updateview']):
        print request.form
        if (dbFleet.Update(request.form)):
            flash('View has been Updated')
        else:
            flash('Opps! Something wrong happened')

    return redirect(url_for('View2'))
    
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

def handle_data(Res, Des):
    Rows = []

    for x in Res:
        Row = []
        for y in Des:
            Index = y[0]
            Row.append(x[Index])
        Rows.append(Row)

    Headers = [x[0] for x in Des]

    return (Headers, Rows)  

if __name__ == '__main__':
    app.run(debug=True)

