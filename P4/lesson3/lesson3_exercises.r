# Lesson 3 exercises

library(ggplot2)
data(diamonds)

summary(diamonds)

ggplot(data = diamonds, aes(x = price)) + geom_histogram() 

#stats
summary(diamonds$price)

#sizes
dim(subset(diamonds, diamonds$price < 500))[1]
dim(subset(diamonds, diamonds$price < 250))[1]
dim(subset(diamonds, diamonds$price >= 15000))[1]

#explore large peak
ggplot(data = diamonds, aes(x = price)) + geom_histogram(binwidth = 1) + 
  scale_x_continuous(limits = c(400, 1000), breaks = seq(0, 1000, 100)) + 
  scale_y_continuous(limits = c(0,150), breaks = seq(0, 150, 5)) +
  ggsave('priceHistogram.png')

# Break out the histogram of diamond prices by cut.
ggplot(data = diamonds, aes(x = price)) + geom_histogram() +
  facet_wrap(~cut)

#stats by cut
by(diamonds$price, diamonds$cut, summary)
by(diamonds$price, diamonds$cut, max)
by(diamonds$price, diamonds$cut, min)

#free scales
qplot(x = price, data = diamonds) + facet_wrap(~cut, scales="free_y")

# Create a histogram of price per carat and facet it by cut.
ggplot(data = diamonds, aes(x = price/carat)) + geom_histogram(binwidth = 0.1) +
  facet_wrap(~cut) + scale_x_log10() + ggsave('pricePerCaratForCutHistogram.png')

#boxplots
ggplot(data = diamonds, aes(x = cut, y = price)) + geom_boxplot()
ggplot(data = diamonds, aes(x = clarity, y = price)) + geom_boxplot()
ggplot(data = diamonds, aes(x = color, y = price)) + geom_boxplot()

#stats
selected_C <- c("D")
price_color_D <- diamonds[diamonds$color  %in% selected_C,]$price
summary(price_color_D)
IQR(price_color_D)

selected_J <- c("J")
price_color_J <- diamonds[diamonds$color  %in% selected_J,]$price
summary(price_color_J)
IQR(price_color_J)

#boxplot price per carat across color
ggplot(data = diamonds, aes(x = color, y = price/carat)) + geom_boxplot()

#frequncy polygon
ggplot(data = diamonds, aes(x = carat)) + geom_freqpoly(binwidth=0.1) + ylim(1000, 12000)

#labour dataset
labour <- read.csv('indicator_labour.csv', header = T, row.names = 1, check.names = F)
labourt <- data.frame(t(labour))
summary(labour)
dim(labour)

#some plots
ggplot(data = labourt, aes(x = Argentina, y = Netherlands)) + geom_boxplot()
ggplot(data = labourt, aes(x = Netherlands)) + geom_histogram(binwidth = 1)
ggplot(data = labourt, aes(x = Netherlands)) + geom_freqpoly(binwidth=0.1)


