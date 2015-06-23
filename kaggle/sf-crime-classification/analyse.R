require(randomForest)

# Address -> Break somehow
# Resolution ???

# Not going to save output in Git so make this as deterministic as possible
set.seed(782629)

out_col_names <- c("ARSON", "ASSAULT", "BAD CHECKS", "BRIBERY", "BURGLARY", 
                   "DISORDERLY CONDUCT", "DRIVING UNDER THE INFLUENCE", 
                   "DRUG/NARCOTIC",  "DRUNKENNESS", "EMBEZZLEMENT", "EXTORTION", 
                   "FAMILY OFFENSES", "FORGERY/COUNTERFEITING", "FRAUD", 
                   "GAMBLING", "KIDNAPPING", "LARCENY/THEFT", "LIQUOR LAWS", 
                   "LOITERING", "MISSING PERSON", "NON-CRIMINAL", 
                   "OTHER OFFENSES", "PORNOGRAPHY/OBSCENE MAT", "PROSTITUTION", 
                   "RECOVERED VEHICLE", "ROBBERY", "RUNAWAY", "SECONDARY CODES", 
                   "SEX OFFENSES FORCIBLE", "SEX OFFENSES NON FORCIBLE", 
                   "STOLEN PROPERTY", "SUICIDE", "SUSPICIOUS OCC", "TREA", 
                   "TRESPASS", "VANDALISM", "VEHICLE THEFT", "WARRANTS", 
                   "WEAPON LAWS")

hours_decimalised <- function(datetime_raw) {
    datetime <- as.numeric(as.POSIXct(datetime_raw, format="%Y-%m-%d %H:%M:%S"))
    date_only <- as.numeric(as.POSIXct(datetime_raw, format="%Y-%m-%d"))
    return((datetime - date_only) / (60 * 60))
}

feature_engineering <- function(filename) {
    df <- read.csv(filename, stringsAsFactors=T)
    df$Date <- as.Date(df$Dates, format ='%Y-%m-%d')
    df$Time <- hours_decimalised(df$Dates)

    # Omit when df$Y == 90 - seems to be a NA value
    df <- subset(df, Y != 90)

    # Scaling coordinates so they are "prettier" to human-interpret
    df$X <- (df$X + 122) * 100
    df$Y <- (df$Y - 37)  * 100

    # Rubbish or variables better engineered in another way
    df$Dates <- NULL
    df$Descript <- NULL
    df$Resolution <- NULL
    df$Address <- NULL      # Removing just for now

    return(df)
}

train <- feature_engineering('train.small.csv')
test <- feature_engineering('test.csv')
fit <- randomForest(Category ~ ., data=train, ntrees=50)
ys <- predict(fit, test[1:10, ])

index_of_result <- function(x) match(x, out_col_names)
result_row <- function(pos) replace(rep(0, length(out_col_names)), pos, 1)

true_indicies <- sapply(ys, index_of_result)
out_df <- data.frame(t(mapply(result_row, true_indicies)))

submission_filename = "submission.csv"
sink(submission_filename)
cat("Id,")
sink()
write.table(out_df, submission_filename, append=T, sep=",", quote=F, 
            col.names=out_col_names,
            row.names=seq(0, length(ys)-1))
