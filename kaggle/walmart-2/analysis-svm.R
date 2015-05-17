library(e1071)

# Not going to save output in Git so make this as deterministic as possible
set.seed(85464)

join_table <- read.csv("key.csv")
weather <- read.csv("weather.csv", stringsAsFactors=T, na.strings=c("M", "  T"))
weather$sunrise <- as.numeric(weather$sunrise)
weather$sunset  <- as.numeric(weather$sunset)

# hack while working with linear model
weather$codesum <- NULL
# this is empty
weather$cool <- NULL

format_input <- function(filename) {
  units_per_day <- read.csv(filename, stringsAsFactors=F)
  units_per_day$date <- as.Date(units_per_day$date, format ='%Y-%m-%d')
  units_per_day <- merge(x=units_per_day, y=join_table, by="store_nbr", all.x=TRUE)
  return(units_per_day)
}

train_units_per_day <- format_input("train.csv")
test_units_per_day  <- format_input("test.csv")

train <- merge(x=train_units_per_day, y=weather, by=c("station_nbr", "date"), all.x=TRUE)
tests <- merge(x=test_units_per_day,  y=weather, by=c("station_nbr", "date"), all.x=TRUE)

model <- svm(units ~ ., data=train, method="anova")

sales <- predict(model, newdata=tests)
result <- data.frame(tests$store_nbr, tests$item_nbr, tests$date, round(sales))
kaggle_fmt <- data.frame(id=paste(result$tests.store_nbr, 
                                  result$tests.item_nbr, 
                                  result$tests.date, 
                                  sep="_"), 
                         units=result$round.sales)

write.csv(kaggle_fmt, "submission-svm.csv", quote=F, row.names=F)