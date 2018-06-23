from statsmodels.tsa.arima_model import ARIMA
from plotly.graph_objs import *
import plotly.graph_objs as go
import plotly.plotly as py
import time, datetime
import io
import math
import database_sqlite as DB
import sqlite3
import pandas as pd

dbname='kufarm.db'
conn=sqlite3.connect(dbname)
curs = conn.cursor()

username = 'pramudityad'
api_key = 'nWvNw18KoFOnL5t8BtDA'
stream_token = 'd5axv933b0'
py.sign_in(username, api_key)

def main():
	sampleFreq = 60
	prediction  = 0
	while True:
		if prediction > 0:
			print (prediction)
			new_row = [(prediction,)]
			curs.executemany("INSERT INTO soil ('forecast') VALUES (?)", new_row)
			conn.commit()
		# fetch the recent readings
		df = pd.read_sql(
		"SELECT * FROM (SELECT * FROM soil ORDER BY created_at DESC LIMIT 150) AS X ORDER BY created_at ASC;", con = conn)

		df['date1'] = pd.to_datetime(df['created_at']).values
		#df['day'] = df['date1'].dt.date
		#df['time'] = df['date1'].dt.time
		df.index = df.date1
		df.index = pd.DatetimeIndex(df.index)
		df = df.drop('forecast',1)
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
		x=X,
		y=[j for j in recentreadings['value'].values],
		    name = 'Outdoor Temperature',
		    line = dict(
		    color = ('rgb(205, 12, 24)'),
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

		trace3 = go.Scatter(
		x = X+X_rev,
		y = y_upper+y_lower,
		    fill='tozerox',
		    fillcolor='rgba(231,107,243,0.2)',
		    line=go.Line(color='transparent'),
		    showlegend=True,
		    name='Confidence Interval'
		)

		data = [trace1, trace2, trace3]

		layout = go.Layout(
		title='Soil Graph',
		yaxis = dict(title = 'Soil Trend Data')
		)

		fig = go.Figure(data=data, layout=layout)

		plot_url = py.plot(fig, filename='soil prediction', auto_open = False)
		
if __name__ == '__main__':
	main()
	time.sleep(60*60)# delay between stream posts