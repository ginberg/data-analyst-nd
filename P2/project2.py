# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 18:54:33 2015
@author: ger
Project 2: Analyzing the NYC Subway Dataset
"""

import csv
import numpy as np
import pandas as pd
import pandasql as pdsql
import matplotlib.pyplot as plt
import scipy.stats
import statsmodels.api as sm
from ggplot import *

def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features. 
    This can be the same code as in the lesson #3 exercise.
    """ 
    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]    
    return intercept, params
    

def compute_r_squared(data, predictions):
    '''
    Calculates R sqared based on given data and predictions
    '''
    SST = ((data - np.mean(data)) **2).sum()
    SSREG = ((predictions - data) **2).sum()
    r_squared = 1 - SSREG / SST
    
    return r_squared

#main
filename='data/improved-dataset/turnstile_weather_v2.csv'
turnstile_weather = pd.read_csv(filename)
print list(turnstile_weather.columns.values)
print turnstile_weather['rain'].describe()

rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 1]
norain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 0]

print len(rain)
print len(norain)

#print "rain-mean:", np.mean(rain_data)
#print "rain-std:",np.std(rain_data)
#print "norain-mean:",np.mean(norain_data)
#print "norain-mean:",np.std(norain_data)

plt.figure()
plt.xlabel('ENTRIESn_hourly ')
plt.ylabel('Frequency')
plt.title('The number of turnstile entries in norain vs rain conditions')
plt.text(2000, 5000, r'blue=no rain, green=rain')
x = [norain, rain]
plt.hist(x, range=(0, 4500), bins=30)

U, p = scipy.stats.mannwhitneyu(rain, norain)
print "U-statistic:", U
print "p-value:", p

#p < 5% so alternative hypotheses applies


#section 2 - lineair regressioon

features = turnstile_weather[['rain', 'hour', 'meantempi', 'weekday']]
dummy_units = pandas.get_dummies(turnstile_weather['UNIT'], prefix='unit')
features = features.join(dummy_units)
# Values
#values = turnstile_weather['ENTRIESn_hourly']
# Perform linear regression
#intercept, params = linear_regression(features, values)

#print "intercept, params", intercept, params
#predictions = intercept + np.dot(features, params)
#print "predictions:", predictions
#print "r-squared:", compute_r_squared(values, predictions)

plot = ggplot(turnstile_weather, aes(x='hour', y='ENTRIESn_hourly', color='rain')) + \
    geom_point() + xlab('hour of day') + ylab('Number of entries') + ggtitle('Number of entries per hour')
print plot





