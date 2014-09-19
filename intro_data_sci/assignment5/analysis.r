#!/usr/bin/Rscript

library(ggplot2)
library(rpart)
library(randomForest)
library(e1071)

input <- read.csv("seaflow_21min.csv", header=TRUE)

print("Question 1")
print(summary(input["pop"]))
# 18146

print("")
print("")

print("Question 2")
print(summary(input["fsc_small"]))
# 39184

print("")
print("")

print("Question 3")
train_length = round(nrow(input) / 2)

shuffled_input <- input[sample(nrow(input), nrow(input)),]
training <- shuffled_input[1: train_length-1, ] 
testing  <- shuffled_input[train_length: nrow(shuffled_input), ]

print(summary(training["time"]))
 

print("")
print("")

print("Question 4")
d <- qplot(input$pe, input$chl_small, data=input, colour=input$pop)
d <- d + geom_point(size=1)
# d
# In the plot of pe vs. chl_small, the particles labeled ultra should 
# appear to be somewhat "mixed" with two other populations of particles. 
# Which two populations?
# Answer: 
#  - pico
#  - nano

print("")
print("")

print("Question 5")

fol <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
model <- rpart(fol, method="class", data=training)
print(model)

# Output:
#  1) root 36171 25755 pico (0.0012 0.18 0.29 0.25 0.28)  
#    2) pe< 5004 26391 16022 pico (0 0.22 0.39 0 0.38)  
#      4) chl_small< 32518.5 11776  2198 pico (0 0.00034 0.81 0 0.19) *
#      5) chl_small>=32518.5 14615  6717 ultra (0 0.41 0.054 0 0.54)  
#       10) chl_small>=41297.5 5287   656 nano (0 0.88 0 0 0.12) *
#       11) chl_small< 41297.5 9328  2086 ultra (0 0.14 0.085 0 0.78) *
#    3) pe>=5004 9780   728 synecho (0.0046 0.051 0.0048 0.93 0.014)  
#      6) chl_small>=39954.5 555    80 nano (0.081 0.86 0 0.032 0.031) *
#      7) chl_small< 39954.5 9225   191 synecho (0 0.0027 0.0051 0.98 0.013) *

# Answer: Crypto ?

print("")
print("")

print("Question 6")

# pe is split at 5004 to follow one path or another (in model above)

print("")
print("")

print("Question 7")

# Based on your decision tree, which variables appear to be most important in
#  predicting the class population?

# pe as it is at the top of the tree

print("")
print("")

print("Question 8")

p_dt <- predict(model, testing)
max_idx <- apply(p_dt, 1, which.max)
o1 <- vapply(max_idx, function(x) colnames(p_dt)[x], FUN.VALUE="")
correct <- (o1 == as.vector(testing["pop"]))
rate <- sum(correct) / nrow(correct)
print(rate)
# 0.8556618

print("")
print("")

print("Question 9")

fol <- formula(pop ~ fsc_small + fsc_perp + chl_small + pe + chl_big + chl_small)
#fol <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)

#model <- randomForest(fol, method="class", data=training)

#p <- predict(model, testing)
#max_idx <- apply(p, 1, which.max)
#o1 <- vapply(max_idx, function(x) colnames(p)[x], FUN.VALUE="")
#correct <- (o1 == as.vector(testing["pop"]))
#rate <- sum(correct) / nrow(correct)

model <- randomForest(fol, data=training)
p_rf <- predict(model,newdata=testing,type="class")
p_rf2 <- as.data.frame(p_rf)
prob1 <- sum(p_rf2[,1] == testing$pop) / nrow(testing)

print(prob1)
# 0.9225368

print("")
print("")

print("Question 10")

print(importance(model))

#           MeanDecreaseGini
# fsc_small         2783.294
# fsc_perp          1797.006
# chl_small         8410.408
# pe                8988.284
# chl_big           4891.920


print("")
print("")

print("Question 11")

model <- svm(fol, data=training)
p_svm <- predict(model, newdata=testing, type="class")
p_svm2 <- as.data.frame(p_svm)
prob2 <- sum(p_svm2[,1] == testing$pop) / nrow(testing)

print(prob2)
# 0.9201316

print("")
print("")

print("Question 12")

print("For Random Forest:")
print(table(pred = p_rf, true = testing$pop))
print("For SVM:")
print(table(pred = p_svm, true=testing$pop))

# Ultra is mistaken for pico

print("")
print("")

print("Question 13")

# fsc_big

print("")
print("")

print("Question 14")

training_no_208 <- training[which(training$file_id != 208),]
testing_no_208 <- testing[which(testing$file_id != 208),]

model <- svm(fol, data=training_no_208)
p_svm3 <- predict(model, newdata=testing_no_208, type="class")
p_svm4 <- as.data.frame(p_svm3)
prob2 <- sum(p_svm4[,1] == testing_no_208$pop) / nrow(testing_no_208)

print(prob2)
# 0.9713243
# So answer: 0.9713243 - 0.9201316 = 0.0511927
