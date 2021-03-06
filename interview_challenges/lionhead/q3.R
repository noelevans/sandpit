dset2 <- read.csv("mod_dataset2.csv", stringsAsFactors=T)
model <- lm(LTD.Revenue ~ ., data=dset2)
tt <- c(T, T)
ff <- c(F, F)
tests <- data.frame(Title.Life.To.Date.months = c(0, 18), 
                    is_console=tt, is_tablet=tt, is_pc=tt, is_phone=ff, 
                    is_fps=tt, is_ccg=tt, is_moba=tt, is_rts=ff,is_adventure=ff)
predict(model, newdata=tests)
