from pandas import Series
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
series = Series.from_csv("D:\\Univ\\Semester 8\\TA 2\\Source Code\\forecast\\new\plot\\soil_test3.csv", header=0)
plot_acf(series)
pyplot.show()