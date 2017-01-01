from sklearn import datasets
from sklearn.cross_validation import cross_val_predict
from sklearn.svm import SVR

import csv as csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib

#load Sample data
readdata = csv.reader(open("result/result.csv"))
datalist = list(readdata)
for row in datalist:
    for k in range(0,15):
        row[k] = float(row[k])
dataset = np.array(datalist).astype(np.float)
X = dataset[:, 1:15]  
y = dataset[:, 0] 
clf = SVR(kernel='rbf', C=1e3, gamma=0.1)
clf.fit(X, y)

#load Predict data
readdata = csv.reader(open("result/predic.csv"))
datalist = list(readdata)
for row in datalist:
    for k in range(0,14):
        row[k] = float(row[k])
dataset = np.array(datalist).astype(np.float)
X2 = dataset[:, 0:14]  

#output to predictor
joblib.dump(clf,"predict/machine_SVR.pkl")

#load predictor
lr=joblib.load("predict/machine_SVR.pkl")
clf.fit(X, y)
predict_y=clf.predict(X2)
predict = clf.predict(X)

plt.scatter(predict,y,s=2)
plt.plot(predict_y, predict_y, 'ro')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Predicted')
plt.ylabel('Measured')
plt.show()
