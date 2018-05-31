import time, datetime
import plotly.plotly as py #plotly library
import plotly.graph_objs as go
from plotly import tools
import sqlite3
import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
#import config

dbname='kufarm.db'
conn=sqlite3.connect(dbname)
curs = conn.cursor()
prediction = 0

while True :
	cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

	if prediction > 0:
		print (prediction)
		new_row = [(prediction,)]
		c.executemany("INSERT INTO soil ('forecast') VALUES (?)", new_row)
		db.commit()
	
	# fetch the recent readings
	df = pd.read_sql(
	"""SELECT *
	FROM (SELECT * FROM soil ORDER BY created_at DESC LIMIT 150)
	AS X
	ORDER BY created_at ASC;""", con = conn)

	df['date1'] = pd.to_datetime(df['created_at']).values
	df['day'] = df['date1'].dt.date
	df['time'] = df['date1'].dt.time
	df.index = df.date1
	df.index = pd.DatetimeIndex(df.index)
	#df = df.drop('forecast',axis=1)
	df['upper'] = df['value']
	df['lower'] = df['value']

	model = ARIMA(df['value'], order=(5,1,0))
	model_fit = model.fit(disp=0)
	forecast = model_fit.forecast(5)
	prediction = round(forecast[0][0],2)
	t0 = df['date1'][-1]
	new_dates = [t0+datetime.timedelta(minutes = 30*i) for i in range(1,6)]
	new_dates1 = map(lambda x: x.strftime('%Y-%m-%d %H:%M'), new_dates)
	df2 = pd.DataFrame(columns=['value','created_at','forecast'])
	df2.date = new_dates1
	df2.forecast = forecast[0]
	df2['upper'] = forecast[0]+forecast[1] #std error
	df2['lower'] = forecast[0]-forecast[1] #std error
	# df2['upper'] = forecast[2][:,1] #95% confidence interval
	# df2['lower'] = forecast[2][:,0] #95% confidence interval
	df = df.append(df2)
	df = df.reset_index()
	recentreadings = df
	recentreadings['forecast'][-6:-5] = recentreadings['value'][-6:-5]

	# plot the recent readings
	X=[str(i) for i in recentreadings['created_at'].values]
	X_rev = X[::-1]
	y_upper = [j for j in recentreadings['upper']]
	y_lower = [j for j in recentreadings['lower']]
	y_lower = y_lower[::-1]

	trace1 = go.Scatter(
	x = X,
	y = [j for j in recentreadings['value'].values],
		name = 'Soil Status',
		line = dict(
		color = ('rgb(22, 96, 167)'),
		width = 4)
	)

	trace2 = go.Scatter(
	x=X,
	y=[j for j in recentreadings['forecast'].values],
		name = 'ARIMA Forecasted Temperature',
		line = dict(
		color = ('rgb(205, 12, 24)'),
		width = 4,
		dash = 'dot')
	)

	data = [trace1, trace2]

	layout = go.Layout(
	title='Soil Graph',
	yaxis = dict(title = 'Value')
	)

	fig = go.Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='soil_predict', auto_open = False)
	time.sleep(60*60)# delay between stream posts
	