import sqlite3
from sqlite3.dbapi2 import Cursor

connection = sqlite3.connect('./static/database/mushroom.db', check_same_thread=False)

my_cursor = connection.cursor()

my_cursor.execute(""" DROP TABLE user_info; """)

my_cursor.execute("""CREATE TABLE user_info(
	"username"	varchar(30) NOT NULL,
	"password"	varchar(30) NOT NULL
);""")

connection.commit()
my_cursor.close()
connection.close()