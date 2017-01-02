from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
import csv as csv
import numpy as np
from sklearn.externals import joblib

#convert predict data to char
def ToChar(numberarray):
	result = []
	for i in range(0,len(numberarray-1)):
		result.append(str(unichr(int(round(numberarray[i])+64))))
	
	return result

def Analysis(userlocation,samplelocation):
	#load Sample data
	readdata = csv.reader(open(samplelocation))
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
	readdata = csv.reader(open(userlocation))
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

	predict = ToChar(predict_y)
	return predict

def AnalysisRealTime(userarray,samplelocation):
	#load Sample data
	readdata = csv.reader(open(samplelocation))
	datalist = list(readdata)
	for row in datalist:
	    for k in range(0,15):
	        row[k] = float(row[k])
	dataset = np.array(datalist).astype(np.float)
	X = dataset[:, 1:15]  
	y = dataset[:, 0] 
	clf = SVR(kernel='rbf', C=1e3, gamma=0.1)
	clf.fit(X, y)  

	#output to predictor
	joblib.dump(clf,"predict/machine_SVR.pkl")

	#load predictor
	lr=joblib.load("predict/machine_SVR.pkl")
	clf.fit(X, y)
	predict_y=clf.predict(userarray)

	predict = str(unichr(int(round(predict_y)+64)))
	return predict