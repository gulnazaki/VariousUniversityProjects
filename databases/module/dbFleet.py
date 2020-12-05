from dbSchema import Table
from flask import flash
from pymysql import Error

import sys

class Fleet(Table):
    def Show(self, licenseplate):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            if (licenseplate == None):
                Cursor.execute("SELECT * FROM `fleet`")
            else:
                SQLQuery = "SELECT * FROM `fleet` where `plate` = %s"

                Cursor.execute(SQLQuery, (licenseplate))

            return Cursor.fetchall()
        except:
            return
        finally:
            Con.close()

    def Update(self, data):
        Con = self.connect()
        Cursor = Con.cursor()

        try:
            UpdateQuery = "UPDATE `fleet` set `plate` = %s, `cartype` = %s, `model` = %s, `make` = %s, `caryear` = %s, `fuel` = %s where `plate` = %s"

            Cursor.execute(UpdateQuery, (data['plate'], data['cartype'], data['model'], data['make'], data['caryear'], data['fuel'], data['plate']))

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