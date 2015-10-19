---
title: 'Analyzing the NYC Subway Dataset'
output: html_document
---

Background Information

In this project, we look at the NYC Subway data and figure out if more people ride the subway when it is raining versus when it is not raining.

##Statistical Test

###1 Independent and dependent variables
 
The independent variable is the rain. It can either be a 0 (no rain) or 1 (rain)
The dependent variable is the the number of entries since the last reading (ENTRIESn_hourly)

The data that is provided is a sample. With the hypothesis tests we want to explore if we can conclude that the subway is used more when it is raining. 
Let μR and μN respectively be the population means for ENTRIESn_hourly when it is not raining and when it is raining. Let H0 and Ha respectively be the 0 and alternative hypothesis. The hypotheses can be written as:

H0 : μR = μN

Ha : μR > μN

When comparing means of populations, multiple tests can be used. A t-test or z-test can be used if the data is assumed to be normally distributed. 
However, the data from our sample is not normally distributed. Mann–Whitney´s U test is a nonparametrict test that can be used if we don't assume that the data follows a certain distribution. Because we don´ t assume any underlying distribution this test will be used. The test will be one tailed, because it is only interesting to know if **more** people use the subway when it is raining.




##Linear Regression

##Visualization

##Conclusion

##Reflection

