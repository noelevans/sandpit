# Taken from here:
# github.com/MattDSquared/BikeSharingDemand/blob/master/BikeShareAnalysis.Rmd

library(dplyr)
library(lubridate)
library(ggplot2)


seasons <- c("spring", "summer", "fall", "winter")
weatherlabels <- c("nice weather", "cloudy/misty", "light weather",
                   "heavy weather")
daysoftheweek <- c("Monday","Tuesday","Wednesday","Thursday","Friday",
                   "Saturday","Sunday")

train <- read.csv("train.csv", stringsAsFactors=F)
train <- mutate(train, 
                datetime = ymd_hms(datetime),
                season = factor(season, levels=1:4, labels=seasons),
                holiday = as.logical(holiday),
                workingday = factor(workingday, levels=c(1,0), 
                                    labels=c("Workday","Holiday/Weekend")),
                weather = factor(weather,levels=1:4, labels=weatherlabels),
                dayofweek = factor(weekdays(datetime), levels=daysoftheweek),
                timeofday = hour(datetime))

tr.inputs <- select(train, datetime:windspeed)
train.svd <- svd(scale(sapply(tr.inputs, unclass)))

gg <- ggplot() + 
    geom_bar(aes(x=1:length(train.svd$d), y=train.svd$d^2/sum(train.svd$d^2)),
             stat="identity",
             fill="dodgerblue") + 
    scale_x_discrete(limits=1:length(tr.inputs)) +
    labs(title="Feature Variance") +
    labs(x="Orthogonal variables") +
    labs(y="Proportion of variance explained")
print(gg)

# Now looking at the 9th axis of PCA since it has little effect on the variance 
# of the data

eigval <- 9
gg <- ggplot() + 
    geom_bar(aes(x=1:length(tr.inputs), y=train.svd$v[,eigval]),
             stat="identity",
             fill="dodgerblue") + 
    scale_x_discrete(limits=names(tr.inputs)) +
    labs(title=paste("Composition of eigenvalue",eigval)) +
    labs(x="Feature") +
    labs(y="Scaled Column Means")
print(gg)