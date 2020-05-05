import json
import pandas as pd


def fn(row):
    if row['Type'] == 'DIRECT DEBIT':
        return 'DD'
    if (row['Type'] == 'DIRECT CREDIT' or 
            row['Spending Category'] in ('INCOME', 'REVENUE')):
        return 'BP'
    if row['Amount (GBP)'] < 0:
        return 'SO'
    print(row)
    raise Exception('Unintended state')


df = pd.read_csv('statement.csv')
conversions = json.load(open('description_conversion.json'))
output = df[['Date']]
output['Type'] = df.apply(fn, axis=1)
output['Description'] = (df['Counter Party'] + ' ' + df['Reference']).replace(conversions)
output['Paid Out'] = df['Amount (GBP)'].copy()
output['Paid In'] = df['Amount (GBP)'].copy()
output['Paid Out'] = output['Paid Out'] * -1
output['Paid Out'][output['Paid Out'] < 0] = None
output['Paid In'][output['Paid In'] < 0] = None
output['Balance'] = df['Balance (GBP)']

output.to_csv('output.csv', index=False)
