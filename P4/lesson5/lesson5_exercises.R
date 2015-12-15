# Create a histogram of diamond prices.
# Facet the histogram by diamond color
# and use cut to color the histogram bars.

library(ggplot2)
ggplot(data = diamonds, aes(x = price)) + 
  geom_histogram(aes(color = cut)) +
  facet_wrap(~color)
  
# Create a scatterplot of diamond price vs.
# table and color the points by the cut of
# the diamond.
ggplot(data = diamonds, aes(x = table, y = price)) + 
  geom_point(aes(color = cut)) +
  xlim(50,80)

# Create a scatterplot of diamond price vs.
# volume (x * y * z) and color the points by
# the clarity of diamonds. Use scale on the y-axis
# to take the log10 of price. You should also
# omit the top 1% of diamond volumes from the plot.

ggplot(data = diamonds, aes(y = price, x = (x*y*z))) + 
  geom_point(aes(color = clarity)) +
  coord_trans(y = "log10") +
  xlim(0,500)

# Your task is to create a new variable called 'prop_initiated'
# in the Pseudo-Facebook data set. The variable should contain
# the proportion of friendships that the user initiated.
pf <- read.csv('../lesson3/pseudo_facebook.tsv', sep = '\t')
pf$prop_initiated = pf$friendships_initiated / pf$friend_count

# Create a line graph of the median proportion of
# friendships initiated ('prop_initiated') vs.
# tenure and color the line segment by
# year_joined.bucket.
pf$year_joined <- floor(2014 - (pf$tenure / 365))
pf$year_joined.bucket <- cut(pf$year_joined, breaks=c(2004, 2009, 2011, 2012, 2014))
ggplot(aes(x = tenure, y = prop_initiated), data = pf) +
  geom_line(aes(color = year_joined.bucket), stat = 'summary', fun.y = median) 

# Smooth the last plot you created of
# of prop_initiated vs tenure colored by
# year_joined.bucket. You can bin together ranges
# of tenure or add a smoother to the plot.
ggplot(aes(x = tenure, y = prop_initiated), data = pf) +
  geom_line(aes(color = year_joined.bucket), stat = 'summary', fun.y = median) +
  geom_smooth()

#group with largest proportion, what is the average proportion
selected<-c("(2012,2014]")
pf_after_2012 <- pf[pf$year_joined.bucket %in% selected,]
pf_after_2012_na <- pf_after_2012[!is.na(pf_after_2012$prop_initiated), ]
mean(pf_after_2012_na$prop_initiated)

# Create a scatter plot of the price/carat ratio
# of diamonds. The variable x should be
# assigned to cut. The points should be colored
# by diamond color, and the plot should be
# faceted by clarity.
ggplot(aes(x = cut, y = price/carat), data = diamonds) +
  geom_point(aes(color = color)) +
  facet_wrap(~clarity)

# The Gapminder website contains over 500 data sets with information about
# the world's population. Your task is to continue the investigation you did at the
# end of Problem Set 4 or you can start fresh and choose a different
# data set from Gapminder.

#labour dataset
labour <- read.csv('../lesson3/indicator_labour.csv', header = T, row.names = 1, check.names = F)
labourt <- data.frame(t(labour))
summary(labour)
dim(labour)

#some plots
ggplot(aes(x = Austria, y = Australia), data = labourt) + 
  geom_point() +
  facet_wrap(~"row.names")
  

  




