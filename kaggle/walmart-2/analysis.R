join_table <- read.csv("key.csv")
weather <- read.csv("weather.csv", stringsAsFactors=T, na.strings=c("M", "  T"))

format_input <- function(filename) {
  units_per_day <- read.csv(filename, stringsAsFactors=F)
  units_per_day$date <- as.Date(units_per_day$date, format ='%Y-%m-%d')
  units_per_day <- merge(x=units_per_day, y=join_table, by="store_nbr", all.x=TRUE)
  return(units_per_day)
}

train_units_per_day <- format_input("train-small.csv")
test_units_per_day  <- format_input("test.csv")

train <- merge(x=train_units_per_day, y=weather, by=c("station_nbr", "date"), all.x=TRUE)
tests <- merge(x=test_units_per_day,  y=weather, by=c("station_nbr", "date"), all.x=TRUE)

model <- lm(units ~ ., data=train)

predict(model, newdata=tests)

