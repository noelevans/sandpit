import pandas as pd


cols = ('Notional', 'Tenor', 'Ccy', 'Cpty')

data = [[  1e7, 6, 'USD', 'JPM'],
        [ 20e6, 3, 'GBP', 'GS'],
        [1.2e6, 1, 'USD', 'JPM'],
        [2.5e9, 1, 'JPY', 'BA'],
        [1.2e7, 1, 'GBP', 'GS']]

df = pd.DataFrame(data, columns=cols)

rates = pd.DataFrame({'Ccy': ['USD', 'GBP', 'JPY'], 'Rate': [1, 0.64, 124.89]})


# Mutable setting. Note it is column, row, value (rather than row, column)

df.set_value(4, 'Tenor', 2)


# Slicing in different directions

print df.loc[:, 'Tenor':'Ccy']
print df.loc[:, ['Tenor','Ccy']]
print df.loc[1:3, :]
print df.loc[1:3, 'Tenor':'Ccy']


# Equal results

print df.loc[3, :]
print df.iloc[3]


# Get a cell value rather than a DataFrame or Series

df.at[3, 'Cpty']        # Fast
df.loc[3, 'Cpty']       # Slow


# Double the notionals

df.Notional = df.Notional * 2


# merge is the function to join tables

usd_all = pd.merge(df, rates, on='Ccy')
usd_all['USD_Notional'] = usd_all.Notional / usd_all.Rate


# concat does a union operation

print pd.concat([df, df])