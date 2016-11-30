import pandas
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder


def main():
    train_all = pandas.DataFrame.from_csv('train.csv')
    train = train_all[['Survived', 'Sex', 'Fare']][:20]

    gender_label = LabelEncoder()
    train.Sex = gender_label.fit_transform(train.Sex)

    X = train[['Sex', 'Fare']]
    y = train['Survived']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42)

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    print(clf.predict(X_test))


if __name__ == '__main__':
    main()
