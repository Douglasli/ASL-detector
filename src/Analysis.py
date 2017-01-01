from sklearn import datasets
from sklearn.cross_validation import cross_val_predict
from sklearn import linear_model
import csv as csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
#load Sample data
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

#load Predict data
lr = linear_model.LinearRegression()
readdata = csv.reader(open("result/predic.csv"))
datalist = list(readdata)
for row in datalist:
    for k in range(0,14):
        row[k] = float(row[k])
dataset = np.array(datalist).astype(np.float)
X2 = dataset[:, 0:14]  
predicted = cross_val_predict(lr, X, y, cv=500)

#output to predictor
joblib.dump(lr,"predict/lr_machine.pkl")

#load predictor
lr=joblib.load("predict/lr_machine.pkl")
lr.fit(X, y)
predict_y=lr.predict(X2)
plt.scatter(predicted,y,s=2)
plt.plot(predict_y, predict_y, 'ro')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Predicted')
plt.ylabel('Measured')
plt.show()
