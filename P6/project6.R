library(ggplot2)
library(caroline)

#read
df <- read.csv("data/246437956_122015_1436_airline_delay_causes.csv", header = TRUE)

#explore
#str(df)
#summary(df)

# univariate plots
#ggplot(data=df, aes(x=carrier_name)) + geom_histogram() 

# bivariate plots
#ggplot(data = df, aes(x=X.weather_ct, y=weather_delay)) + geom_point()
#ggplot(data = df, aes(x=weather_delay, y=late_aircraft_delay)) + geom_point()
#carries vs carrier
#ggplot(data = df_by_carrier, aes(x=carrier, y=total_delay)) + geom_point()

#feature engineering
#X.arr_delay is total delay!
#df$total_delay <- df$X.arr_delay + df$X.carrier_delay + df$weather_delay + df$nas_delay + df$security_delay + df$late_aircraft_delay

#str(df$total_delay)
#group tot_delay by carrier and year
df_by_carrier <- aggregate(cbind(X.arr_delay, X.carrier_delay, weather_delay, nas_delay, security_delay, late_aircraft_delay) ~ carrier + carrier_name + year, df, sum)
names(df_by_carrier)[names(df_by_carrier)=="X.arr_delay"] <- "total_delay"
names(df_by_carrier)[names(df_by_carrier)=="X.carrier_delay"] <- "carrier_delay"
delayTypes <- c("total_delay", "carrier_delay", "weather_delay", "nas_delay", "security_delay", "late_aircraft_delay")

#add relative delays for individual years
#approach: 
#loop over years
# loop over delays
#   for each delay add a column to df
#for each year merge this df to total_df
df_by_carrier_total <- df_by_carrier[0:0,]
years <- unique(df_by_carrier$year)
for (i in 1:length(years)){
  year <- years[i]
  delays_per_year <- df_by_carrier[df_by_carrier$year == year,]
  #init df
  for (delayType in delayTypes){
    df_by_carrier_delay_year <- delays_per_year[,c(delayType)]
    total <- sum(df_by_carrier_delay_year)
    delayVariable <- paste0(delayType,"_rel")
    delays_per_year[[delayVariable]] <- df_by_carrier_delay_year / total
  }
  df_by_carrier_total <- merge(df_by_carrier_total, delays_per_year, all=TRUE)
}

#add relative delays for all years
df_by_carrier_total <- pct(df_by_carrier_total, c("total_delay", "carrier_delay", "weather_delay", "nas_delay", "security_delay", "late_aircraft_delay"))

#write processed df to file
write.csv(df_by_carrier_total, "data/246437956_122015_1436_airline_delay_causes_result.csv", row.names = FALSE)

#generate a sample set to increase development speed
#df_result <- df_by_carrier[sample(nrow(df_by_carrier), 100),]