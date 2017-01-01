from sklearn import datasets
from sklearn.cross_validation import cross_val_predict
from sklearn import linear_model
import csv as csv
import numpy as np
import matplotlib.pyplot as plt
lr = linear_model.LinearRegression()
readdata = csv.reader(open("result/result.csv"))
datalist = list(readdata)
for row in datalist:
    for k in range(0,15):
        row[k] = float(row[k])
dataset = np.array(datalist).astype(np.float)
X = dataset[:, 1:15]  
y = dataset[:, 0] 
predicted = cross_val_predict(lr, X, y, cv=500)

fig, ax = plt.subplots()
ax.scatter(y, predicted)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()
