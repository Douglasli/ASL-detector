from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
import csv as csv
import numpy as np
from sklearn.externals import joblib

def ToChar(numberarray):
	result = []
	for i in range(0,len(numberarray-1)):
		result.append(str(unichr(int(round(numberarray[i])+64))))
	
	return result
def Predict():
	#load Predict data
	readdata = csv.reader(open("result/user.csv"))
	datalist = list(readdata)
	for row in datalist:
	    for k in range(0,14):
	        row[k] = float(row[k])
	dataset = np.array(datalist).astype(np.float)
	X2 = dataset[:, 0:14]  
	clf = SVR(kernel='rbf', C=1e3, gamma=0.1)

   	clf=joblib.load("predict/machine_SVR.pkl")
   	
	predict_y=clf.predict(X2)

	predict = ToChar(predict_y)
	return predict