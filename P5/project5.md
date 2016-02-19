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
Next, I have done some exploratory data analysis. One of the first things I noticed, is that there are only 146 observations (people) in the dataset.
Of these 146, 18 persons are a poi and 128 are not. There are 21 features per person.

I have created a function, plotFeatures, to be able to plot 2 features against each other. In that way, it is possible to see if there are outliers.
A useful plot is the salary vs bonus plot. There is a huge outlier called 'TOTAL' in this plot. After investigation, this is the total value of salary
and bonus for all the people in the dataset! So, this observation should be removed from the dataset.

Because I noticed quite a lot of NaN values, I have looked at persons with many NaN's. There were 5 people with 18 or more NaN values. 
One of these is named 'THE TRAVEL AGENCY IN THE PARK'. Because this is clearly not an employee of Enron, this observation is also removed from the dataset.

Machine learning algorithms normally normally can't handle NaN values very good, so these should be handled. Most of the features have an integer
value and some have a string value.

## Feature selection

I have used SelectKBest to select the best features from the input features. The input features are the features that were supplied from the dataset plus 1 have added. 
My ideal behind this feature is, that a poi might be given a relatively high bonus compared to others. That is why I have added a bonus to salary feature.


## Algorithm

I have tried multiple algorithms to see the effect on accuracy. As said in the introduction, I need to use a classification algorithm. The package sklearn
provides multiple of these algorithms that I can use, SVM, nearest neighbors, decision trees or an ensemble method like random forests.
I have added these classifiers to the pipeline one by one and looked at the effect on the accuracy, precision and recall. Some algorithms had a better performance
before parameter tuning than others while others improved quite a lot with parameter tuning.
In the end, I had the best performance with the DecisionTreeClassifier so I have choses this algorithm.

## Algorithm tuning

With algorithm tuning a better performance can be made.
I have used GridSearchCV to tune my algorithm.


## Validation strategy

StratifiedShuffleSplit


## Evaluation metrics

Accuracy/ Precision/ Recall