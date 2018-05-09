import sqlite3 as lite
import sys
con = lite.connect('kufarm.db')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS DHT_data")
    cur.execute("CREATE TABLE DHT_data(ID INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
