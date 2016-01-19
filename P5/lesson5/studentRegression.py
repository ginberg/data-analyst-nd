# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 11:44:23 2016

@author: ger
"""
from agesnetworth import ageNetWorthData
from sklearn import linear_model

def studentReg(ages_train, net_worths_train):
    ### import the sklearn regression module, create, and train your regression
    ### name your regression reg
    
    ### your code goes here!
    clf = linear_model.LinearRegression()
    reg = clf.fit (ages_train, net_worths_train)
    return reg


ages_train, ages_test, net_worths_train, net_worths_test = ageNetWorthData()

reg = studentReg(ages_train,net_worths_train)

print reg.predict([27])
print reg.coef_[0][0]
print reg.intercept_

print "r-sqared-score train:", reg.score(ages_train, net_worths_train)
print "r-sqared-score test:",reg.score(ages_test, net_worths_test)
