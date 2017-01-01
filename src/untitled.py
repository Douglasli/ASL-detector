import numpy as np
import csv as csv

readdata = csv.reader(open("result/result.csv"), delimiter=',')
datalist = list(readdata)
for row in datalist:
    for k in range(0,14):
        row[k] = float(row[k])


print(datalist)