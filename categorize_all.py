# analyse.py
# This script takes a CSV data file of feature data and group them into two groups:
# 1. response time small or equal to 1 hour.
# 2. response time greater than 1 hour.

import csv
import sys
import numpy as np
import math
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold


def write_to_output(data, output):
    writer = csv.writer(output)
    for row in data:
        writer.writerow(row)

def group_data(data):
    grouped_data = []
    
    for value in data:
        if(value < 3600): #time less than one hour
            grouped_data.append(0)
        #elif(value < 14400): #time less than 4 hour
        #    grouped_data.append(1)
        #elif(value < 43200): #time less than 12 hour
        #    grouped_data.append(2)
        #elif(value < 86400): #time less than 24 hour
        #    grouped_data.append(3)
        else: 
            grouped_data.append(1)
    
    return grouped_data
    
def categorize():
    print('Loading data...')
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    print('Separating data...')
    X = np.array([ x[:7] for x in data ]).astype(float)
    Y = np.array([ x[7] for x in data ]).astype(float)

    print('Labelling data...')
    features_with_grouped_times = np.insert(X, 7, group_data(Y), axis=1)

    print('Writing data to file...')
    write_to_output(features_with_grouped_times, open(sys.argv[2], 'w', newline=''))
               
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 categorize_all.py features.csv labeledfeatures.csv')
        sys.exit(1)

    categorize()
    
    
    
    

