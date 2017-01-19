from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
import csv as csv
import numpy as np
from sklearn.externals import joblib

def ToChar(numberarray):
	datalist = {'a':1,'b':2,'c':3,'k':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'d':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26,'0':27,'1':28,'2':29,'3':30,'4':31,'5':32,'6':33,'7':34,'8':35,'9':36}
	result = []
	for i in range(0,len(numberarray-1)):
		result.append(datalist.keys()[datalist.values().index(int(round(numberarray[i])))])
	
	return result
def Predict():
	#load Predict data
	readdata = csv.reader(open("result/user.csv"))
	datalist = list(readdata)
	for row in datalist:
	    for k in range(0,20):
	        row[k] = float(row[k])
	dataset = np.array(datalist).astype(np.float)
	X2 = dataset[:, 0:20]  
	clf = SVR(kernel='rbf', C=1e3, gamma=0.1)

   	clf=joblib.load("predict/machine_SVR.pkl")
   	
	predict_y=clf.predict(X2)

	predict = ToChar(predict_y)
	return predict