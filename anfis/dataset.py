import csv
import itertools
temperature = [30,30,30,30]
humidity = [10,30,60,90]
soil = [60,120,240,360]
rain = [6,12,24,36]

dataset = open("dataset.csv","w")
with open('dataset.csv',newline='') as f:
    r = csv.reader(f)
    wr = csv.writer(dataset ,quoting=csv.QUOTE_ALL)
    data = [line for line in r]

with open('dataset.csv','w',newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['temperature','humidity','soil','rain'])
    wr.writerows(list(itertools.product(temperature,humidity,soil,rain)))
    wr.writerows(data)