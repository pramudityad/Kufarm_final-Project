import itertools
import csv
temperature = [30,30,30,30]
humidity = [10,30,60,90]
soil = [120,240,360,480]
rain = [60,120,240,360]

dataset = open("dataset.csv","w")
wr = csv.writer(dataset ,quoting=csv.QUOTE_ALL)
wr.writerows(list(itertools.product(temperature,humidity,soil,rain)))