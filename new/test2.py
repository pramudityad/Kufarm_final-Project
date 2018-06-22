import database_sqlite as DB
import sqlite3
import time, datetime
import wunderground as WU

dbname='kufarm.db'
conn=sqlite3.connect(dbname)
curs = conn.cursor()

am = WU.getpop(0)
pm = WU.getpop(1)
am_condition = WU.getweather(0)
pm_condition = WU.getweather(1)
wsp = "wunderground"
now = datetime.datetime.now()
timeRequest = now.strftime('%Y-%m-%d %H:00:00');

DB.addForecast2(am,pm,am_condition,pm_condition,wsp,timeRequest)

