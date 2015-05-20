library(e1071)
library(plyr)

# Not going to save output in Git so make this as deterministic as possible
set.seed(85464)

format_input <- function(filename) {
  units_per_day <- read.csv(filename, stringsAsFactors=F)
  units_per_day$date <- as.Date(units_per_day$date, format ='%Y-%m-%d')
  units_per_day <- merge(x=units_per_day, y=join_table, by="store_nbr", all.x=TRUE)
  return(units_per_day)
}

fit_for_weather_stn <- function(train_set) {
  print(train_set$station_nbr[1])
  model <- svm(units ~ ., data=train_set)
  weather_stn_tests <- subset(tests, station_nbr == train_set$station_nbr[1])
  sales <- predict(model, newdata=weather_stn_tests)
  result <- data.frame(store_nbr=weather_stn_tests$store_nbr, 
                       item_nbr=weather_stn_tests$item_nbr, 
                       date=weather_stn_tests$date, 
                       sales=round(sales))
  return(result)
}

join_table <- read.csv("key.csv")
weather <- read.csv("weather.csv", stringsAsFactors=T, na.strings=c("M", "  T"))
weather$sunrise <- as.numeric(weather$sunrise)
weather$sunset  <- as.numeric(weather$sunset)

# hack while working with linear model
weather$codesum <- NULL
# this is empty
weather$cool <- NULL

# assume NAs to be zero to start
weather[is.na(weather)] <- 0

train_units_per_day <- format_input("train.csv")
test_units_per_day  <- format_input("test.csv")

train <- merge(x=train_units_per_day, y=weather, by=c("station_nbr", "date"))
tests <- merge(x=test_units_per_day,  y=weather, by=c("station_nbr", "date"))

train_by_weather_stn <- split(train, as.factor(train$station_nbr))

all_results <- lapply(train_by_weather_stn, fit_for_weather_stn)
result <- rbind.fill(all_results)

kaggle_fmt <- data.frame(id=paste(result$store_nbr, 
                                  result$item_nbr, 
                                  result$date, 
                                  sep="_"), 
                         units=result$sales)

write.csv(kaggle_fmt, "submission-svm.csv", quote=F, row.names=F)
