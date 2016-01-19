from prep_terrain_data import makeTerrainData
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from class_vis import prettyPicture, output_image

import matplotlib.pyplot as plt
import copy
import numpy as np
import pylab as pl

features_train, labels_train, features_test, labels_test = makeTerrainData()
########################## SVM #################################
### we handle the import statement and SVC creation for you here

def fitPredictAndPrintAccuracy(clf):
    #### now your job is to fit the classifier
    #### using the training features/labels, and to
    #### make a set of predictions on the test data
    clf.fit(features_train, labels_train)
    #### store your predictions in a list named pred
    pred = clf.predict(features_test)    
    acc = accuracy_score(pred, labels_test)
    print acc

clf = SVC(kernel="linear")
fitPredictAndPrintAccuracy(clf)
prettyPicture(clf, features_test, labels_test)

#Parameters in Machine Learning
clf = SVC(kernel="linear", gamma=1.0)
fitPredictAndPrintAccuracy(clf)
prettyPicture(clf, features_test, labels_test)

