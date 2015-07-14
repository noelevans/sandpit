from sklearn.linear_model import LogisticRegression


class MultivariateLogisticOvrModel(object):

    def model_and_predict(self, X_train, y_train, X_test):
        model = LogisticRegression(dual=True, fit_intercept=True, 
                                   multi_class='ovr')
        model.fit(X_train, y_train)
        return model.predict(X_test)


class MultivariateLogisticMultinomialModel(object):

    def model_and_predict(self, X_train, y_train, X_test):
        model = LogisticRegression(dual=False, fit_intercept=False, 
                                   multi_class='multinomial')
        model.fit(X_train, y_train)
        return model.predict(X_test)

