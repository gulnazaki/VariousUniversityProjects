
from dbSchema import Table

class Reserve(Table):
    def ShowReserves(self, licenseplate, startdate):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            if (licenseplate == None) or (startdate == None):
                Cursor.execute("SELECT * FROM reserves order by startdate asc")
            else:
                SQLQuery = "SELECT * FROM `reserves` where `licenseplate` = %s and `startdate` = %s order by `startdate` asc"

                Cursor.execute(SQLQuery, (licenseplate, startdate))

            return Cursor.fetchall()
        except:
            return
        finally:
            Con.close()

    def AddReserve(self, NewData):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            InsertQuery = """\
            INSERT INTO reserves (licenseplate, startdate, finishdate, 
            startlocation, finishlocation, paid, customerid) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""

            Cursor.execute(InsertQuery, (NewData['licenseplate'], 
                NewData['startdate'], NewData['finishdate'], 
                NewData['startlocation'], NewData['finishlocation'], 
                NewData['paid'], NewData['customerid']))

            """ Commit the Query """
            Con.commit()
            
            return True
        except :

            """ This method sends a ROLLBACK statement to the MySQL server, 
            undoing all data changes from the current transaction. By default, 
            Connector/Python does not autocommit, so it is possible to cancel 
            transactions when using transactional storage engines such as InnoDB. """

            Con.rollback()
            
            return False
        finally:
            Con.close()

    def UpdateReserve(self, UpdatedData):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            UpdateQuery = """\
            UPDATE `reserves` set `licenseplate` = %s, `startdate` = %s, `finishdate` = %s, \
             `startlocation` = %s, `finishlocation` = %s, `paid` = %s, `customerid` = %s \
             where `licenseplate` = %s and `startdate` = %s"""

            Cursor.execute(UpdateQuery, (UpdatedData['licenseplate'], 
                UpdatedData['startdate'], UpdatedData['finishdate'], 
                UpdatedData['startlocation'], UpdatedData['finishlocation'], 
                UpdatedData['paid'], UpdatedData['customerid'],
                UpdatedData['licenseplate'], UpdatedData['startdate']))

            """ Commit the Update """
            Con.commit()
            
            return True
        except :

            """ This method sends a ROLLBACK statement to the MySQL server, 
            undoing all data changes from the current transaction. By default, 
            Connector/Python does not autocommit, so it is possible to cancel 
            transactions when using transactional storage engines such as InnoDB. """

            Con.rollback()
            
            return False
        finally:
            Con.close()

    def DeleteReserve(self, Data):

        Con = self.connect()
        Cursor = Con.cursor()

        try:
            DeleteQuery = "DELETE FROM `reserves` WHERE `licenseplate`= %s and `startdate` = %s"

            Cursor.execute(DeleteQuery, (Data['licenseplate'], Data['startdate']))

            """ Commit the Delete """
            Con.commit()
            
            return True
        except :

            """ This method sends a ROLLBACK statement to the MySQL server, 
            undoing all data changes from the current transaction. By default, 
            Connector/Python does not autocommit, so it is possible to cancel 
            transactions when using transactional storage engines such as InnoDB. """

            Con.rollback()
            
            return False
        finally:
            Con.close()
