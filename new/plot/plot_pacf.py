from pandas import Series
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_pacf
series = Series.from_csv("D:\\Damar x220\\Damar\\Univ\\Semester 8\\TA 2\\Source Code\\forecast\\new\\plot\\soil_test3.csv", header=0)
plot_pacf(series, lags=50)
pyplot.show()