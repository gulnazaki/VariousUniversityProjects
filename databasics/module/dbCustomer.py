
from dbSchema import Table

class Customer(Table):
    def ShowCustomers(self, id):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            if (id == None):
                Cursor.execute("SELECT * FROM `customer` order by `customerid`")
            else:
                SQLQuery = "SELECT * FROM `customer` where `customerid` = %s order by `customerid` asc"

                Cursor.execute(SQLQuery, (id))

            return Cursor.fetchall()
        except:
            return
        finally:
            Con.close()

    def AddCustomer(self, NewData):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            InsertQuery = """\
            INSERT INTO customer (irsnumber, firstname, 
            lastname, SocialSecurityNo, DriverLicense, FirstRegistration,
            City, Street, StreetNo, PostalCode) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            Cursor.execute(InsertQuery, (NewData['irsnumber'], 
                NewData['firstname'], NewData['lastname'], 
                NewData['socialsecurityno'], NewData['driverlicense'], 
                NewData['firstregistration'], NewData['city'], NewData['street'],
                NewData['streetno'], NewData['postalcode']))

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

    def Hi(self, UpdatedData, id):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            UpdateQuery = """\
            UPDATE `customer` set `irsnumber` = %s, `firstname` = %s, `lastname` = %s, \
             `SocialSecurityNo` = %s, `DriverLicense` = %s, `FirstRegistration` = %s, \
             `City` = %s, `Street` = %s, `StreetNo` = %s, `PostalCode` = %s \
             where `customerid` = %s"""

            Cursor.execute(UpdateQuery, (UpdatedData['irsnumber'], 
                UpdatedData['firstname'], UpdatedData['lastname'], 
                UpdatedData['socialsecurityno'], UpdatedData['driverlicense'], 
                UpdatedData['firstregistration'], UpdatedData['city'], UpdatedData['street'],
                UpdatedData['streetno'], UpdatedData['postalcode'], id))

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

    def DeleteCustomer(self, customerid):

        Con = self.connect()
        Cursor = Con.cursor()

        try:
            DeleteQuery = "DELETE FROM `customer` WHERE `customerid` = %s"

            Cursor.execute(DeleteQuery, (customerid))

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
