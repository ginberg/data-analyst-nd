# lesson 4 exercises

library(ggplot2)
data(diamonds)
summary(diamonds)

ggplot(data = diamonds, aes(x = x, y = price)) + geom_point() 

# correlation
with(diamonds, cor.test(x, price))
with(diamonds, cor.test(y, price))
with(diamonds, cor.test(z, price))

#scatter price vs depth
ggplot(data = diamonds, aes(x = depth, y = price)) + geom_point() 

ggplot(data = diamonds, aes(x = depth, y = price)) + 
  geom_point(alpha = 1/100) +
  scale_x_continuous(breaks = seq(43, 79, 2))

# correlation
with(diamonds, cor.test(depth, price))

#scatter price vs carat
ggplot(data = diamonds, aes(x = carat, y = price)) + geom_point() 

#scatter price vs volume
diamonds$volume <- diamonds$x * diamonds$y * diamonds$z
ggplot(data = diamonds, aes(x = volume, y = price)) + geom_point() 

# correlation
diamonds_vol_0_800 <- subset(diamonds, volume > 0 & volume < 800)
with(diamonds_vol_0_800, cor.test(volume, price))

ggplot(data = diamonds_vol_0_800, aes(x = volume, y = price)) + 
  geom_point(alpha=1/100) +
  geom_smooth(method = "lm", color = "red")

#dplyr
suppressMessages(library(ggplot2))
suppressMessages(library(dplyr))
diamondsByClarity <- diamonds %>% 
  group_by(clarity) %>%
  summarise(mean_price  = mean(price),
            median_price  = median(price),
            min_price  = min(price),
            max_price  = max(price),
            n = n()) %>%
  arrange(clarity)
head(diamondsByClarity) 

# bar charts of mean price
diamonds_by_clarity <- group_by(diamonds, clarity)
diamonds_mp_by_clarity <- summarise(diamonds_by_clarity, mean_price = mean(price))

diamonds_by_color <- group_by(diamonds, color)
diamonds_mp_by_color <- summarise(diamonds_by_color, mean_price = mean(price))

diamonds_by_cut <- group_by(diamonds, cut)
diamonds_mp_by_cut <- summarise(diamonds_by_cut, mean_price = mean(price))

install.packages("gridExtra")
library(gridExtra)

plotPriceByClarity <- ggplot(diamonds_mp_by_clarity, aes(y = mean_price, x=clarity)) + geom_bar(stat="identity")
plotPriceByColor <- ggplot(diamonds_mp_by_color, aes(y = mean_price, x=color)) + geom_bar(stat="identity")
plotPriceByCut <- ggplot(diamonds_mp_by_cut, aes(y = mean_price, x=cut)) + geom_bar(stat="identity")
grid.arrange(plotPriceByClarity, plotPriceByColor,plotPriceByCut)

#labour dataset
labour <- read.csv('../lesson3/indicator_labour.csv', header = T, row.names = 1, check.names = F)
labourt <- data.frame(t(labour))
summary(labour)
dim(labour)

#some plots
ggplot(aes(x = Austria, y = Australia), data = labourt) + geom_point() + geom_smooth()

