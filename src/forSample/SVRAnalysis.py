from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
import csv as csv
import numpy as np
from sklearn.externals import joblib


def main():
	#load Sample data
	readdata = csv.reader(open("../result/sample.csv"))
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
	joblib.dump(clf,"../predict/machine_SVR.pkl")

if __name__ == "__main__":
    main()