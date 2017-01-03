from sklearn import datasets
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.externals import joblib
import csv as csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score

# lr = linear_model.LinearRegression()
readdata = csv.reader(open("../result/sample.csv"))
datalist = list(readdata)
for row in datalist:
    for k in range(0,15):
        row[k] = float(row[k])
dataset = np.array(datalist).astype(np.float)
X = dataset[:, 1:15]  
y = dataset[:, 0] 

clf=joblib.load("../predict/machine_SVR.pkl")
clf.fit(X, y)

predict=clf.predict(X)
print clf.score(X, y)
scores=cross_val_score(clf,X,y,cv=8)
print scores
plt.scatter(predict,y,s=2)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Predicted')
plt.ylabel('Measured')
plt.show()
