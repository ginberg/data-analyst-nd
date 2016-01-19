# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 14:22:40 2016
@author: ger
"""
import sklearn.linear_model.Lasso

features, labels = GetMyData()
regression = Lasso()
regression.fit(features, labels)