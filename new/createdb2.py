import sqlite3 as lite
import sys
con = lite.connect('kufarm.db')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS soil")
    cur.execute("CREATE TABLE soil (ID INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, value int NUMERIC)")
