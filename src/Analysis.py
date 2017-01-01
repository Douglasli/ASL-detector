import numpy as np
import csv as csv
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
from sklearn import datasets
import math

#Read file
readdata = csv.reader(open("result/result.csv"))
datalist = list(readdata)
for row in datalist:
    for k in range(0,14):
        row[k] = float(row[k])
dataset = np.array(datalist).astype(np.float)
print(dataset.shape)
X = dataset[:, 1:9]  
y = dataset[:, 0] 
label_dict = {1: 'A', 4: 'D'}
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12,6))
feature_dict = {i:label for i,label in zip(
                range(8),
                  ('T_MtoP',
                  'T_PtoI',
                  'T_ItoD',
                  'I_MtoP', 
                  'I_PtoI',	
                  'I_ItoD',	
                  'M_MtoP',	
                  'M_PtoI'))}
for ax,cnt in zip(axes.ravel(), range(8)):  

    # set bin sizes
    min_b = math.floor(np.min(X[:,cnt]))
    max_b = math.ceil(np.max(X[:,cnt]))
    bins = np.linspace(min_b, max_b, 25)

    # plottling the histograms
    for lab,col in zip([1,4], ('blue', 'red')):
        ax.hist(X[y==lab, cnt],
                   color=col,
                   label='class %s' %label_dict[lab],
                   bins=bins,
                   alpha=0.5,)
    ylims = ax.get_ylim()

    # plot annotation
    leg = ax.legend(loc='upper right', fancybox=True, fontsize=8)
    leg.get_frame().set_alpha(0.5)
    ax.set_ylim([0, max(ylims)+2])
    ax.set_xlabel(feature_dict[cnt])
    ax.set_title('Iris histogram #%s' %str(cnt+1))

    # hide axis ticks
    ax.tick_params(axis="both", which="both", bottom="off", top="off",  
            labelbottom="on", left="off", right="off", labelleft="on")

    # remove axis spines
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)    

axes[0][0].set_ylabel('count')
axes[1][0].set_ylabel('count')

fig.tight_layout()       

plt.show()

