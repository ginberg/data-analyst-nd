## Summarization project goal and the usefullness of machine learning

In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. 
In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails 
and detailed financial data for top executives. Based on this data, I have identified persons that have caused this scandal, the people are referred to as people 
of interest (poi).


## Feature selection

I have used SelectKBest to select the best features from the input features. The input features are the features that were supplied from the dataset plus 1 have added. 
My ideal behind this feature is, that a poi might be given a relatively high bonus compared to others. That is why I have added a bonus to salary feature.


## Algorithm

I have used a DecisionTreeClassifier


## Algorithm tuning

I have used GridSearchCV to tune my algorithm


## Validation strategy




## Evaluation metrics

Precision/Recall
