import numpy as np
import pandas as pd
 
 
def rename_unis(df, renames):
    """ Update institution if they appear in the renames dictionary. """
 
    for before, after in renames.items():
        df.ix[df.institution == before, 'institution'] = after
    return df
 
 
def main():
    """ Read some university records and analyse. """
 
    newer_records = pd.read_csv('2016_to_2017.csv', sep='\t')
    older_records = pd.read_csv('2012_to_2014.csv', sep='\t')
 
    newer_records = newer_records.rename(
        columns={'Institution': 'institution'})
 
    new_renames = {'Newman': 'Newman University',
                   "St Mary's": "St Mary's UC",
                   'Leeds Beckett': 'Leeds Met',
                   'University Campus Suffolk': 'UC Suffolk'}
    newer_records = rename_unis(newer_records, new_renames)
 
    old_renames = {'Glynd': 'Glyndwr'}
    older_records = rename_unis(older_records, old_renames)
 
    recs = pd.merge(newer_records, older_records,
                    how='outer', on='institution')
 
    # Fix outer join null values
    recs = recs.fillna(501)
 
    # Fix columns
    recs.columns = [2017, 2016, 'institution', 2014, 2013, 2012]
    recs = recs[['institution', 2012, 2013, 2014, 2016, 2017]]
    years = recs.columns.values[1:].astype('int')
 
    # Different ways of calculating the mean
    recs['mean'] = recs[list(years)].mean(axis=1)
    recs['mean'] = recs.mean(axis=1)
    my_mean = lambda xs: sum(xs[1:]) / len(xs[1:])
    recs['mean'] = recs.apply(my_mean, axis=1)
 
 
    # Add decay_mean: weights are heavier for dates closer to today
    half_life = 5   # (years)
    today = 2016 + 1
    elapsed_time = today - years
 
    # very aggresive decay weights
    weights = np.e ** - (elapsed_time * half_life)
    # more even weighting but still bias towards recent data
    weights = 0.5 ** (elapsed_time / half_life)
    print(weights)
 
    decay_mean = lambda x: sum(x * weights) / sum(weights)
    recs['decay_mean'] = recs[list(years)].apply(decay_mean, axis=1)
 
    print('Order by 2017')
    print(recs.sort(2017)[:10])
    print('Order by mean')
    print(recs.sort('mean')[:10])
    print('Order by decay mean')
    print(recs.sort('decay_mean')[:10])


if __name__ == '__main__':
    main()
