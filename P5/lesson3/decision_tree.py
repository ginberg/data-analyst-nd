# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 17:42:04 2016
@author: ger
"""
#!/usr/bin/python

""" lecture and example code for decision tree unit """

import sys
sys.path.append("../lesson1/")
from class_vis import prettyPicture, output_image
from prep_terrain_data import makeTerrainData

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import math
#from classifyDT import classify
from sklearn import tree
from sklearn.metrics import accuracy_score

features_train, labels_train, features_test, labels_test = makeTerrainData()

def classify():
    clf = tree.DecisionTreeClassifier(min_samples_split=2)
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    acc = accuracy_score(pred, labels_test)
    print acc
    return clf

### the classify() function in classifyDT is where the magic
### happens--it's your job to fill this in!
#clf = classify()

#### grader code, do not modify below this line

#prettyPicture(clf, features_test, labels_test)
#output_image("test.png", "png", open("test.png", "rb").read())

def entropy(p, base):
    return (p * math.log(p, base))

# entropy on grade
print -entropy(0.5, 2)

entropy_steep = -(entropy(0.666666, 2) + entropy(0.333333, 2))
print entropy_steep

#information gain = entropy_parent - entropyy_children
gain = 1 - 0.75 * entropy_steep
print gain