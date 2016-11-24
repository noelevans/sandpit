import pandas


def main():
    train_all = pandas.DataFrame.from_csv('train.csv')
    train = train_all[['Survived', 'Sex', 'Fare']]
    print(train)


if __name__ == '__main__':
    main()
