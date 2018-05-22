import MySQLdb as dbapi
import sys
import csv

QUERY='SELECT * FROM kufarm.soil.value, kufarm.rain.value, kufarm.dht11;'
db=dbapi.connect(host='localhost',user='root',passwd='')

cur=db.cursor()
cur.execute(QUERY)
result=cur.fetchall()

c = csv.writer(open('dbdump01.csv', 'wb'))
for x in result:
	c.writerow(x)