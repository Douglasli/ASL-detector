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
    for k in range(0,20):
        row[k] = float(row[k])
dataset = np.array(datalist).astype(np.float)
X = dataset[:, 1:20]  
y = dataset[:, 0] 
clf = SVR(kernel='rbf', C=1e3, gamma=0.1)
clf=joblib.load("../predict/machine_SVR.pkl")

predict=clf.predict(X)
print clf.score(X, y)
fig = plt.figure(figsize=(10, 5), dpi=200)

plt.scatter(predict,y,s=2,color='red')
for a in range(1,37):
	plt.plot([a-0.5,a+0.5], [a,a],color='blue',linestyle="-")
#annotate
datalist = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26,'0':27,'1':28,'2':29,'3':30,'4':31,'5':32,'6':33,'7':34,'8':35,'9':36}
for a in range(1,37):
	text = datalist.keys()[datalist.values().index(a)]
	plt.annotate(text,
 	            xy=(a, a), xycoords='data',xytext=(+0, +3), textcoords='offset points',fontsize=10)

#configure  X axes
plt.xlim(0,38)
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])

#configure  Y axes
plt.ylim(0,38)
plt.yticks([1,4,8,12,16,20,24,28,32,36,37])

#label
plt.xlabel('Predicted')
plt.ylabel('Measured')
plt.show()
