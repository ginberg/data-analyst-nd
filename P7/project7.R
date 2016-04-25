#standard deviation
baseline <- read.csv("final_baseline.csv", header = FALSE)
df <- as.data.frame(t(baseline))
df<-data.frame()
df <- rbind(df, baseline$V2)
#colnames(df) <- as.vector(baseline$V1)
colnames(df) <- c("pageviews_pd", "clicks_pd", "enrollments_pd", "ct_prob", "enroll_prob", "payment_enroll_prob", "payment_click_prob")

calcSD <- function(p,n){
  return(sqrt((p * (1-p) / n)))
}
#sd gross conversion, calculate with binomial distribution
sample_size <- 5000
n <- sample_size * df$ct_prob
calcSD(df$enroll_prob, n)

#sd net conversion
n <- sample_size * df$ct_prob
calcSD(df$payment_click_prob, n)

#samplesize
samplesize <- function(alpha, beta, p, dmin) {
  z.alpha <- qnorm(1 - alpha/2)
  z.beta <- qnorm(1 - beta)
  se.null.numerator <- sqrt(2*p*(1 - p))
  se.alt.numerator <- sqrt(p*(1 - p) + (p + dmin)*(1 - (p + dmin)))
  size <- ((z.alpha*se.null.numerator + z.beta*se.alt.numerator) / dmin)^2
  return(size)
}

#gross
gross_sample_size <- round(samplesize(0.05, 0.20, 0.20625, 0.01))

#net
net_sample_size <- round(samplesize(0.05, 0.20, 0.1093125, 0.0075))

#calculate pageviews by click through rate and multiply by 2 because sample size is per variation 
gross_pageviews <- gross_sample_size * (1/df$ct_prob) * 2
net_pageviews <- net_sample_size * (1/df$ct_prob) * 2
pageviews <- max(gross_pageviews, net_pageviews)

#length of experiment
days <- ceiling(max(gross_pageviews, net_pageviews) / df$pageviews_pd)

##sanity checks
control <- read.csv("final_results_control.csv", header = TRUE)
exp <- read.csv("final_results_experiment.csv", header = TRUE)
control_tot_pageviews <- sum(control$Pageviews)
exp_tot_pageviews <- sum(exp$Pageviews)
#number of cookies
sd_pageviews <- calcSD(0.5, control_tot_pageviews + exp_tot_pageviews)
ME_pageviews <- 1.96 * sd_pageviews
CI_low <- 0.5 - ME_pageviews
CI_high <- 0.5 + ME_pageviews
observed <- control_tot_pageviews / (control_tot_pageviews + exp_tot_pageviews)

#number of clicks on free trial
control_tot_clicks <- sum(control$Clicks)
exp_tot_clicks <- sum(exp$Clicks)
sd_clicks <- calcSD(0.5, control_tot_clicks + exp_tot_clicks)
ME_clicks <- 1.96 * sd_clicks
CI_low <- 0.5 - ME_clicks
CI_high <- 0.5 + ME_clicks
observed <- control_tot_clicks / (control_tot_clicks + exp_tot_clicks)


##effect size tests



## sign test
number_of_experiments <- 23
gross_conversion_successes <- c(19)
net_conversion_successes <- c(13)

binom.test(gross_conversion_successes, number_of_experiments, p = 0.5, alternative = c("two.sided", "less", "greater"), conf.level = 0.95)
binom.test(net_conversion_successes, number_of_experiments, p = 0.5, alternative = c("two.sided", "less", "greater"), conf.level = 0.95)
