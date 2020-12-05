from dbSchema import Table
from flask import flash
from pymysql import Error

import sys

class Rent(Table):
    def ShowRents(self, licenseplate, startdate):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            if (licenseplate == None) or (startdate == None):
                Cursor.execute("SELECT * FROM `rents`")
            else:
                SQLQuery = "SELECT * FROM `rents` where `licenseplate` = %s  and `startdate` = %s order by `startdate` asc"

                Cursor.execute(SQLQuery, (licenseplate, startdate))

            return Cursor.fetchall()
        except:
            return
        finally:
            Con.close()

    def AddRent(self, NewData):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            InsertQuery = """\
            INSERT INTO rents(licenseplate, startdate, finishdate, 
            startlocation, finishlocation, customerid, returnstate, irsnumber,
            paymentamount, paymentmethod) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            Cursor.execute(InsertQuery, (NewData['licenseplate'], 
                NewData['startdate'], NewData['finishdate'], 
                NewData['startlocation'], NewData['finishlocation'], 
                NewData['customerid'], NewData['returnstate'], NewData['irsnumber'],
                NewData['paymentamount'], NewData['paymentmethod']))

            """ Commit the Query """
            Con.commit()
            
            return True
        except:

            """ This method sends a ROLLBACK statement to the MySQL server, 
            undoing all data changes from the current transaction. By default, 
            Connector/Python does not autocommit, so it is possible to cancel 
            transactions when using transactional storage engines such as InnoDB. """

            Con.rollback()
            
            return False
        finally:
            Con.close()

    def UpdateRent(self, UpdatedData):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            UpdateQuery = """\
            UPDATE `rents` set `licenseplate` = %s, `startdate` = %s, `finishdate` = %s, \
             `startlocation` = %s, `finishlocation` = %s, `customerid` = %s, \
             `returnstate` = %s, irsnumber = %s, paymentamount = %s, paymentmethod = %s \
             where `licenseplate` = %s and `startdate` = %s"""

            Cursor.execute(UpdateQuery, (UpdatedData['licenseplate'], 
                UpdatedData['startdate'], UpdatedData['finishdate'], 
                UpdatedData['startlocation'], UpdatedData['finishlocation'], UpdatedData['customerid'],
                UpdatedData['returnstate'], UpdatedData['irsnumber'], UpdatedData['paymentamount'], 
                UpdatedData['paymentmethod'], UpdatedData['licenseplate'], UpdatedData['startdate']))

            """ Commit the Update """
            Con.commit()
            
            return True
        except:

            """ This method sends a ROLLBACK statement to the MySQL server, 
            undoing all data changes from the current transaction. By default, 
            Connector/Python does not autocommit, so it is possible to cancel 
            transactions when using transactional storage engines such as InnoDB. """

            Con.rollback()
            
            return False
        finally:
            Con.close()

    def DeleteRent(self, Data):

        Con = self.connect()
        Cursor = Con.cursor()

        try:
            DeleteQuery = "DELETE FROM rents WHERE `licenseplate`= %s and `startdate` = %s"

            Cursor.execute(DeleteQuery, (Data['licenseplate'], Data['startdate']))

            """ Commit the Delete """
            Con.commit()
            
            return True
        except:

            """ This method sends a ROLLBACK statement to the MySQL server, 
            undoing all data changes from the current transaction. By default, 
            Connector/Python does not autocommit, so it is possible to cancel 
            transactions when using transactional storage engines such as InnoDB. """

            Con.rollback()
            
            return False
        finally:
            Con.close()
