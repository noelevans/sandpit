library(nnet)

cars  <- data.frame(Speed  = c(  47,     49,      32,      27,        12,      11),
                    Colour = c("Red", "Red", "Other", "Other",  "Purple", "Purple"))
cars$Colour <- as.factor(cars$Colour)

model <- multinom(Colour ~ Speed, family=binomial, data=cars)

predict(model, newdata=data.frame(Speed = c(48)))
predict(model, newdata=data.frame(Speed = c(30)))
predict(model, newdata=data.frame(Speed = c( 9)))

summary(model)
