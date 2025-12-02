#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 22:17:04 2025

@author: quentinjonneaux
"""

import pandas as pd # Pandas for data reading and manipulation
import numpy as np # Numpy for mathematical calculation and manipulating arrays
from sklearn import metrics # Scikit Learn metrics for computing confusion matrices and accuracy scores
from sklearn import model_selection # Scikit Learn model_selection to apply K-Fold cross validation
from sklearn import neighbors # Scikit Learn neighbors for creating a KNN
from sklearn import linear_model # Scikit Learn linear model for creating a Perceptron
from sklearn import tree # Scikit Learn tree for creating a decision tree
from sklearn import svm # Scikit Learn svm for creating a support vector machine
import matplotlib.pyplot as plt

path = '/Users/quentinjonneaux/Desktop/ Experiment/Coursera/financial_transactions_dataset.csv'

df=pd.read_csv(path)

features = df.drop('is_fraud',axis=1)
target = df['is_fraud']



# Feature Engineering

# Transaction time

features['timestamp'] = pd.to_datetime(features['timestamp'])

features['trans_date_year'] = features['timestamp'].dt.strftime('%Y')
features['trans_date_year'] = features['trans_date_year'].astype(int)

features['trans_date_month'] = features['timestamp'].dt.strftime('%m')
features['trans_date_month'] = features['trans_date_month'].astype(int)

features['trans_date_day'] = features['timestamp'].dt.strftime('%d')
features['trans_date_day'] = features['trans_date_day'].astype(int)

features['trans_date_hour'] = features['timestamp'].dt.strftime('%H')
features['trans_date_hour'] = features['trans_date_hour'].astype(int)
                                       
features['trans_date_minute'] = features['timestamp'].dt.strftime('%M')
features['trans_date_minute'] = features['trans_date_minute'].astype(int)

features['trans_date_second'] = features['timestamp'].dt.strftime('%S')
features['trans_date_second'] = features['trans_date_second'].astype(int)

features=features.drop('timestamp',axis=1)


# Categories

# Dummies
# for var in features[['merchant','category','city','state','job']].columns:
#     dummies = pd.get_dummies(features[var],dtype=int)
#     features = pd.concat([features,dummies],axis=1).drop(var,axis=1)


# Replace

#get all categorical columns
cat_columns = features.select_dtypes(['object']).columns

#convert all categorical columns to numeric
features[cat_columns] = features[cat_columns].apply(lambda x: pd.factorize(x)[0])

# Trans_num
features=features.drop('transaction_id',axis=1)

print('preprocessing done')


# clf = neighbors.KNeighborsClassifier(n_neighbors=4, metric='minkowski')
# clf = linear_model.Perceptron()
# clf = tree.DecisionTreeClassifier()
clf = svm.SVC(gamma=float(1e-6))

# Split set into training set (80% of data) and test set (20% of data) with n sample of data
test_features, train_features, test_labels, train_labels = model_selection.train_test_split(features,
                                                                                            target,
                                                                                            test_size=0.8,
                                                                                            random_state=0,
                                                                                            stratify=target)

clf.fit(train_features, train_labels)
print('training done')
preds = clf.predict(test_features)
print('predictions done')
confusion_matrix = metrics.confusion_matrix(test_labels, preds)
print('Confusion matrix: ',confusion_matrix)
accuracy = metrics.accuracy_score(test_labels, preds)
print('Accuracy score: ',accuracy)

disp = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix,
                              display_labels=clf.classes_)
disp.plot()
plt.show()