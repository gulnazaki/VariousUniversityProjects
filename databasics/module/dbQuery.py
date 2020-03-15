from dbSchema import Table
import pymysql

class Query(Table):
	def ExecQuery(self, SQLQuery):
		Con = self.connect()
		Cursor = Con.cursor(pymysql.cursors.DictCursor)

		try:
			Cursor.execute(SQLQuery)

			return (Cursor.fetchall(), Cursor.description)
		except:

			return (None, None)
		finally:
			Con.close()