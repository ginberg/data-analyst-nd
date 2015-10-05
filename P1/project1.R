# Report some descriptive statistics regarding this dataset. Include at least one measure of central tendency and at least one measure of variability.

# Read stroop performance csv file
performance <- read.csv("data/stroop-performance.csv", sep=",", header=TRUE);
congruent <- performance$Congruent;
incongruent <- performance$Incongruent;

mean(congruent);
sd(congruent)
mean(incongruent);
sd(incongruent);

#4. Provide one or two visualizations that show the distribution of the sample data. Write one or two sentences noting what you observe about the plot or plots.

hist(congruent, col=rgb(1,0,0,0.5), main="Frquency of times for congruent vs incongruent word list", xlab="Time (s)")
hist(incongruent, col=rgb(0,0,1,0.5), add=T)

# In the histogram the data of both the congruent (red) and incongruent (blue) list is displayed. As can be seen, some people finished
# the congruent list within 10 seconds, where as the fastest for the inncongruent list is about 15sec. From 15 sec to 20sec
# there is quite some overlap between the 2 lists but after that it is almost only the incongruent data that is present.
#The difference in averages for the two lists as calculated in the last exercise (14sec vs 22 sec) is clearly visible in the plot.

#5. Now, perform the statistical test and report your results. 
# What is your confidence level and your critical statistic value? 
#Do you reject the null hypothesis or fail to reject it? Come to a conclusion in terms of the experiment task. 
#Did the results match up with your expectations?

diff <- incongruent - congruent;
diff;
mean(diff);
sd(diff);
# t critival value for a confidence level of 5%. Two sided so use 0.975
qt(c(.025, .975), 23);
t.test(incongruent, congruent, var.equal=FALSE, paired=TRUE)
#6. Optional: What do you think is responsible for the effects observed? 
# Can you think of an alternative or similar task that would result in a similar effect? 
#Some research about the problem will be helpful for thinking about these two questions!

