from pandas import Series
from matplotlib import pyplot
series = Series.from_csv('D:\\Univ\\Semester 8\\TA 2\\BUKU TA\\New folder\\Buku new\\file\\sampling_hum.csv', header=0)
pyplot.plot(series)
pyplot.title('Sampling Kelembapan Udara')
pyplot.show()