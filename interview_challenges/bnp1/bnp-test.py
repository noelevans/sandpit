import argparse
import logging
import pandas as pd
from xml.dom import minidom


logging.basicConfig(
        filename='server.log', 
        level=logging.INFO, 
        format='%(asctime)-15s %(levelname)-8s %(message)s'
    )
log = logging.getLogger()


def classify(row):
    if row['Value'] > row['Limit']:
        return 'Rejected'
    if row['NumberOfTrades'] > row['Count']:
        return 'Pending'
    if row['NumberOfTrades'] < row['Count']:
        log.warning('Too many fills for ID: %s', row.name)
    return 'Accepted'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    input_filename = parser.parse_args().input_file
    log.info('========================')
    log.info('Reading file: %s', input_filename)
    dom = minidom.parse(input_filename)

    rows = []
    for t in dom.getElementsByTagName('Trade'):
        row = dict(t.attributes.items())
        row['Value'] = t.firstChild.data
        rows.append(row)

    log.info('Reading %i trade fills', len(rows))
    df = pd.DataFrame(rows, dtype=int)
    counts = df['CorrelationId'].value_counts()
    counts.name = 'Count'
    aggregators = {'Limit': 'max', 'NumberOfTrades': 'max', 'Value': 'sum'}
    agg = df.groupby('CorrelationId', as_index=True).agg(aggregators)
    agg = agg.join(pd.DataFrame(counts))
    agg['State'] = agg.apply(classify, axis=1)
    result = agg.sort_values('CorrelationId').to_csv(
            'results.csv',
            columns=['NumberOfTrades', 'State'],
            index=True
        )
    log.info('Finished fill processing')


if __name__ == '__main__':
    main()

