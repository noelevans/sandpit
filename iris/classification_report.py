from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split


def main():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=2)

    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X_train, y_train)
    y_hat = clf.predict(X_test)

    print(y_test == y_hat)
    print(classification_report(
        y_test, y_hat, target_names=iris.target_names))



if __name__ == '__main__':
    main()
