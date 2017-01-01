from sklearn import datasets
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.externals import joblib
import csv as csv
import numpy as np
import matplotlib.pyplot as plt
# lr = linear_model.LinearRegression()
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

joblib.dump(clf,"predict/machine_SVR.pkl")
clf=joblib.load("predict/machine_SVR.pkl")
clf.fit(X, y)

predict=clf.predict(X)
clf.score(X, y)

plt.scatter(predict,y,s=2)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Predicted')
plt.ylabel('Measured')
plt.show()
