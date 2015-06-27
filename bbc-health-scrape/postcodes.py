import pandas as pd


def district_postcodes(filename):
    # read csv file
    df = pd.read_csv(filename, sep=',')[['Postcode', 'District']]
    # group by county, select first postcode
    return df.groupby(by='District').first()


def main():
    print district_postcodes('postcodes.csv')


if __name__ == '__main__':
    main()