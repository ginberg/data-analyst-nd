library(ggplot2)
library(caroline)

#read
df <- read.csv("data/246437956_122015_1436_airline_delay_causes.csv", header = TRUE)

#explore
str(df)
summary(df)

# univariate plots
#ggplot(data=df, aes(x=carrier_name)) + geom_histogram() 

# bivariate plots
#ggplot(data = df, aes(x=X.weather_ct, y=weather_delay)) + geom_point()
#ggplot(data = df, aes(x=weather_delay, y=late_aircraft_delay)) + geom_point()
#carries vs carrier
#ggplot(data = df_by_carrier, aes(x=carrier, y=total_delay)) + geom_point()

#feature engineering
df$total_delay <- df$X.arr_delay + df$X.carrier_delay + df$weather_delay + df$nas_delay + df$security_delay + df$late_aircraft_delay

#str(df$total_delay)
#group tot_delay by carrier and year
df_by_carrier <- aggregate(cbind(X.arr_delay, X.carrier_delay, weather_delay, nas_delay, security_delay, late_aircraft_delay, total_delay) ~ carrier + carrier_name + year, df, sum)
total_delays_per_year <- aggregate(total_delay ~ year, df_by_carrier, sum)
#years <- c("2010")
df_by_carrier_total <- df_by_carrier[0:0,]
for (i in 1:length(total_delays_per_year$year)){
  year <- total_delays_per_year[[1]][i]
  total <- total_delays_per_year[[2]][i]
  df_by_carrier_year <- df_by_carrier[df_by_carrier$year == year,]
  df_by_carrier_year$total_delay_rel <- df_by_carrier_year$total_delay / total
  df_by_carrier_total <- merge(df_by_carrier_total, df_by_carrier_year, all=TRUE)
}
  
df_by_carrier_total <- pct(df_by_carrier_total, c("X.arr_delay", "X.carrier_delay", "weather_delay", "nas_delay", "security_delay", "late_aircraft_delay", "total_delay"))

#generate a sample set to increase development speed
#df_result <- df_by_carrier[sample(nrow(df_by_carrier), 100),]

#write processed df to file
write.csv(df_by_carrier_total, "data/246437956_122015_1436_airline_delay_causes_result.csv", row.names = FALSE)

#test <- data.frame(a=c(1,2,3), b=c('x','y','z'), c=c(5,3,2))
#pct(test, c('a','c'))



