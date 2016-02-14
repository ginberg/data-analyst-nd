#!/usr/bin/python

import sys
import pickle
sys.path.append("../../ud120-projects/tools/")
import csv, os
from itertools import compress

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
import matplotlib.pyplot

from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
from sklearn.feature_selection import SelectKBest
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
feature_of_interest = ['poi']
financial_features =  ['salary', 'deferral_payments', 'total_payments', 
                       'loan_advances', 'bonus', 'restricted_stock_deferred', 
                       'deferred_income', 'total_stock_value', 'expenses', 
                       'exercised_stock_options', 'other','long_term_incentive', 
                       'restricted_stock', 'director_fees']
email_features =      ['to_messages', 'from_poi_to_this_person', 
                       'from_messages', 'from_this_person_to_poi', 
                       'shared_receipt_with_poi']
features_list = feature_of_interest + financial_features + email_features

### Load the dictionary containing the dataset
with open("data/final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

def datasetExploration():    
    print('Dataset Exploration')
    print('Number of data points: %d' % len(data_dict.keys()))
    data_dict.keys()
    poi_count = 0
    for name in data_dict.keys():
        person_dict = data_dict[name]
        if person_dict['poi'] == True:
            poi_count += 1
    print('Number of poi: %d' % poi_count)
    print('Number of non-poi: %d' % (len(data_dict.keys()) - poi_count))

def writeDataToCsv(filename):
    try:
        os.remove(filename)
    except OSError:
        pass
    with open(filename, 'a') as fp:
        writer = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        header = ["name", "salary", "to_messages", "deferral_payments", "total_payments", "exercised_stock_options", "bonus",
                  "restricted_stock", "shared_receipt_with_poi", "restricted_stock_deferred", "total_stock_value",
                  "expenses", "loan_advances", "from_messages", "other", "from_this_person_to_poi", "poi", "director_fees",
                  "deferred_income", "long_term_incentive" , "email_address", "from_poi_to_this_person"]
        writer.writerow(header)
        for name in data_dict.keys():
            person_dict = data_dict[name]
            props = [name]
            for prop in person_dict:
                props.append(person_dict[prop])
            writer.writerow(props)
    print('Content written to %s' % filename)

#datasetExploration()
#writeDataToCsv("data/enron.csv")

### Task 2: Remove outliers

### plot features X and Y against each other
def plotFeatures(X, Y):
    for key in data_dict:
        value = data_dict[key]
        salary = value[X]
        bonus = value[Y]
        matplotlib.pyplot.scatter( salary, bonus )
    matplotlib.pyplot.xlabel(X)
    matplotlib.pyplot.ylabel(Y)
    matplotlib.pyplot.show()

#plotFeatures('from_poi_to_this_person', 'from_this_person_to_poi')
#plotFeatures('salary', 'bonus')
#plotFeatures('total_payments', 'total_stock_value')
salary_bonus_outlier_list = [k for k in data_dict.keys() 
        if data_dict[k]["salary"] != 'NaN' and data_dict[k]["salary"] > 1000000 and data_dict[k]["bonus"] > 10000000]
print salary_bonus_outlier_list
payments_outlier_list = [k for k in data_dict.keys() 
        if data_dict[k]["total_payments"] != 'NaN' and data_dict[k]["total_payments"] > 100000000]

def checkPersonsWithManyNaNValues():
    for person in data_dict:
        count = 0
        personDict = data_dict[person]
        for key in personDict:
            value = personDict[key]
            if value == 'NaN':
                count += 1
        if count >= 18:
            print person
#checkPersonsWithManyNaNValues()

""" removes list of outliers keys from dict object """
def remove_outliers(dict_object, keys):
    for key in keys:
        dict_object.pop(key, 0)

print "Removing outliers"
outliers = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK']
remove_outliers(data_dict, outliers)

# replace NaN values
def replaceNaNValues():
    print "Replace NaN's"
    for person in data_dict:
        personDict = data_dict[person]
        for key in personDict:
            value = personDict[key]
            if value == 'NaN':
                if key == 'email_address':
                    personDict[key] = ''
                else:
                    personDict[key] = 0

replaceNaNValues()
#writeDataToCsv("data/enron_clean.csv")

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

#function to compute the feaction given numerator (num) and denumerator (denum)
def compute_fraction(num, denum):
    if num == 0 or denum == 0:
        return 0.
    return float(num) / denum

#add feature bonus / salary, because a poi might get a relative high bonus
bonus_to_salary_feature = 'bonus_to_salary'
fraction_from_poi_feature = 'fraction_from_poi'
fraction_to_poi_feature = 'fraction_to_poi'
for key in my_dataset:
    value = my_dataset[key]
    salary = value['salary']
    bonus = value['bonus']
    salary = int(salary)
    bonus = int(bonus)
    value[bonus_to_salary_feature] = compute_fraction(bonus, salary)
    from_poi_to_this_person = value["from_poi_to_this_person"]
    to_messages = value["to_messages"]
    value[fraction_from_poi_feature] = compute_fraction(from_poi_to_this_person, to_messages)
    from_this_person_to_poi = value["from_this_person_to_poi"]
    from_messages = value["from_messages"]
    value[fraction_to_poi_feature] = compute_fraction(from_this_person_to_poi, from_messages)
        
# add the features to the list
features_list = features_list + [bonus_to_salary_feature, fraction_from_poi_feature, fraction_to_poi_feature]

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)
features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size=0.3, random_state=42)

#select top 10 features to use
#selectedFeatures = selector.fit(features, labels)
#feature_names = [features_list[i+1] for i in selectedFeatures.get_support(indices = True)]
#print "SelectKBest features:", feature_names

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
#clf = GaussianNB()
#scaler = MinMaxScaler()
#knn = KNeighborsClassifier()

scaler = MinMaxScaler()
selector = SelectKBest()
decisionTreeClasssifier = tree.DecisionTreeClassifier()
estimators = [('scaler', scaler), ('selector', selector), ('tree', decisionTreeClasssifier)]
pipeline = Pipeline(estimators)
pipeline.fit(features_train, labels_train)
pred = pipeline.predict(features_test)
acc = accuracy_score(pred, labels_test)
print "accuracy:", acc

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

# parameterss for decision tree
param_grid = [{
                'selector__k': [5,10,20,'all'],    
                'tree__criterion': ['gini', 'entropy'],
                'tree__splitter': ['best', 'random'],
                'tree__max_depth': [1,2,3,4,5,6,7,8],
                'tree__min_samples_split': [1,2,3,4,5,6,7,8]
             }]

# add StratifiedShuffleSplit for cross validation. It improves perforamnce because it keeps in mind the relative occurence of labels
cv = StratifiedShuffleSplit(labels, random_state=42)
gridSearch = GridSearchCV(pipeline, param_grid, cv=cv)
gridSearch.fit(features, labels)
pred = gridSearch.predict(features_test)
acc = accuracy_score(pred, labels_test)
# return the best estimator as input for tester.py!
clf = gridSearch.best_estimator_
print "accuracy with gridsearch:", acc
print "best_estimator:", clf
#print clf.named_steps['selector'].get_support()
features = clf.named_steps['selector']
support = features.get_support()
features_list_without_poi = features_list[:]
del features_list_without_poi[0]
#print chosen features
print "selected_features:", list(compress(features_list_without_poi, support))

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)