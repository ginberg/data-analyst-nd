# Identify Fraud from Enron Email

## Introduction

In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. 
In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails 
and detailed financial data for top executives. Based on this data, I have identified persons that have caused this scandal, the people are referred to as people 
of interest (poi).

To identify a poi, I haved used machine learning algorithms. Machine learning is a type of artificial intelligence (AI) 
that provides computers with the ability to learn without being explicitly programmed. Because the enron dataset already contains if a person is 
a poi, I will use supervised algorithms. The idea of such an algorithm is the find the underlying patterns that determine the outcome feature (poi). 
Furthermore, the algorithm to use will be a classifier, because the output feature has only 2 possible outcomes, True or False.


## Dataset exploration and cleaning

First, I have explored the dataset. Because the input file is in a format that is hard to read, I have transformed it to a csv file.

TODO: outliers
TODO:exploration

## Feature selection

I have used SelectKBest to select the best features from the input features. The input features are the features that were supplied from the dataset plus 1 have added. 
My ideal behind this feature is, that a poi might be given a relatively high bonus compared to others. That is why I have added a bonus to salary feature.


## Algorithm

I have tried multiple classifiers to see the effect on the accuracy. 

So, for the final I have used a DecisionTreeClassifier.


## Algorithm tuning

With algorithm tuning a better performance can be made.
I have used GridSearchCV to tune my algorithm.


## Validation strategy

StratifiedShuffleSplit


## Evaluation metrics

Accuracy/ Precision/ Recall