# analyse.py
# This script takes a CSV data file of feature data. It runs the times through
# RandomForestClassifier to check its accuracy.
# You can run the same file against the same file. i.e. analyse_all.py file1.csv file1.csv if you want to perform train + test on the same file
# However, the cross-val with 10-fold is always performed on the first file. 
import time
import csv
import sys
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print('Usage: python3 analyse_all.py labeledfeature1.csv labeledfeature2.csv')
        sys.exit(1)

    print('Loading data...')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'r') as f2:
        reader = csv.reader(f)
        data = list(reader)
        reader2 = csv.reader(f2)
        data2 = list(reader2)	
	

    print('Separating data...') #X is the data and y is the label
    X_train = np.array([ x[:7] for x in data ]).astype(float)
    y_train = np.array([ x[7] for x in data ]).astype(float)
    X_test = np.array([ x[:7] for x in data2 ]).astype(float)
    y_test = np.array([ x[7] for x in data2 ]).astype(float)


    print('fitting...')
    rf = RandomForestClassifier(random_state=1, n_estimators = 100)
    rf.fit(X_train,y_train)
    print('calculating...')
    start = time.time()
    print("\nPredict all using rf:", rf.predict(X_test))
    end = time.time()   
    print('Time spend: ', end - start)
    print("\nSuccess rate rf:", rf.score(X_test, y_test))
    rfscores = cross_val_score(rf, X_train, y_train, cv = 10)
    print("\nSuccess rate rf in cross val on training dataset:", rfscores)
	