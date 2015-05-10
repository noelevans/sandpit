join_table <- read.csv("key.csv")

units_per_day <- read.csv("train-small.csv", stringsAsFactors=F)
units_per_day$date <- strptime(units_per_day$date, format ='%Y-%m-%d')
units_per_day <- merge(x=units_per_day, y=join_table, by="store_nbr", all.x=TRUE)

weather <- read.csv("weather.csv", stringsAsFactors=T, na.strings=c("M", "  T"))

train <- merge(x=units_per_day, y=weather, by=c("station_nbr", "date"), all.x=TRUE)

