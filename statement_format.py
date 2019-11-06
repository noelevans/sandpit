import pandas as pd


def fn(row):
    if row['Type'] == 'DIRECT DEBIT':
        return 'DD'
    if row['Type'] == 'DIRECT CREDIT' or row['Spending Category'] == 'INCOME':
        return 'BP'
    if row['Amount (GBP)'] < 0:
        return 'SO'
    raise Exception('Unintended state')


df = pd.read_csv('statement.csv')
output = df[['Date']]
output['Type'] = df.apply(fn, axis=1)
output['Description'] = df['Reference']
output['Paid Out'] = df['Amount (GBP)'].copy()
output['Paid In'] = df['Amount (GBP)'].copy()
output['Paid Out'] = output['Paid Out'] * -1
output['Paid Out'][output['Paid Out'] < 0] = 0
output['Paid In'][output['Paid In'] < 0] = 0
output['Balance'] = df['Balance (GBP)']

print(output)
