import pymysql

class Table():
    def connect(self):
        return pymysql.connect("localhost","root","1","database")