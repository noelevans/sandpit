import optparse
import random

import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

# Dependent variables to resolve:
# Address -> Break somehow
# Resolution ???


parser = optparse.OptionParser()

parser.add_option('--full', action='store_true', default=False)
options, args = parser.parse_args()

print 'Full value:', options.full


if options.full:
    print "Running full execution of training/test data"
    train_filename = "train.csv"
    test_filename = "test.csv"
    independent_vars = ['DayOfWeek', 'Date', 'Time', 'X', 'Y']
    n_trees = 2
else:
    print "Running with a subset of training/test data"
    train_filename = "train.small.csv"
    test_filename = "test.small.csv"
    independent_vars = ['DayOfWeek']
    n_trees = 1


CATEGORICAL_VARS = ('DayOfWeek', 'PdDistrict')
OUT_COL_NAMES = ("ARSON", "ASSAULT", "BAD CHECKS", "BRIBERY", "BURGLARY",
                 "DISORDERLY CONDUCT", "DRIVING UNDER THE INFLUENCE",
                 "DRUG/NARCOTIC",  "DRUNKENNESS", "EMBEZZLEMENT", "EXTORTION",
                 "FAMILY OFFENSES", "FORGERY/COUNTERFEITING", "FRAUD",
                 "GAMBLING", "KIDNAPPING", "LARCENY/THEFT", "LIQUOR LAWS",
                 "LOITERING", "MISSING PERSON", "NON-CRIMINAL",
                 "OTHER OFFENSES", "PORNOGRAPHY/OBSCENE MAT", "PROSTITUTION",
                 "RECOVERED VEHICLE", "ROBBERY", "RUNAWAY", "SECONDARY CODES",
                 "SEX OFFENSES FORCIBLE", "SEX OFFENSES NON FORCIBLE",
                 "STOLEN PROPERTY", "SUICIDE", "SUSPICIOUS OCC", "TREA",
                 "TRESPASS", "VANDALISM", "VEHICLE THEFT", "WARRANTS",
                 "WEAPON LAWS")


def feature_engineering(filename, is_training=False, encoders={}):
    df = pd.read_csv(filename)
    temp = pd.DatetimeIndex(df['Dates'])
    df['Date'] = temp.date
    df['Time'] = temp.time

    # Rubbish or variables better engineered in another way
    del df['Dates']
    del df['Address']         # Removing just for now

    if not encoders:
        for c in CATEGORICAL_VARS:
            all_choices = tuple(set(df[c]))
            le = preprocessing.LabelEncoder()
            le.fit(all_choices)
            encoders[c] = le

    for c in CATEGORICAL_VARS:
        df[c] = encoders[c].transform(df[c])
            
    if is_training:
        # df['Category'] = df['Category'].astype(object)

        # Omit when df$Y == 90 - seems to be a NA value
        df = df[df['Y'] != 90]

        del df['Descript']
        del df['Resolution']

    # Scaling coordinates so they are "prettier" to human-interpretation
    df['X'] = (df['X'] + 122) * 100
    df['Y'] = (df['Y'] -  37) * 100

    return df, encoders


train, encoders = feature_engineering(train_filename, is_training=True)
test, _ = feature_engineering(test_filename, encoders=encoders)

districts = set(train['PdDistrict'])
district_ys = {}

# Grow forest and predict separately for each district's records
for d in districts:
    district_name = encoders['PdDistrict'].inverse_transform(d)
    district_train = train[train['PdDistrict'] == d]
    district_train = district_train.drop(['PdDistrict'], axis=1)
    district_test = test[test['PdDistrict'] == d]
    district_test = district_test.drop(['PdDistrict'], axis=1)
    print "Growing forest for", district_name

    # Not saving output in Git so make this deterministic with random_state
    rf = RandomForestClassifier(n_estimators=n_trees, n_jobs=-1, 
                                random_state=782629)
    rf.fit(district_train[independent_vars], 
           list(district_train['Category']))

    district_ys[d] = rf.predict(district_test[independent_vars])
    print "Finished", district_name

print "All predictions made"

ys = []
for i, row in test.iterrows():
    d_ys = district_ys[row['PdDistrict']]
    ys.append(d_ys[0])
    d_ys = d_ys[1:]

# index_of_result = function(x) match(x, OUT_COL_NAMES)
# result_row = function(pos) replace(rep(0, length(OUT_COL_NAMES)), pos, 1)

# true_indicies = sapply(ys, index_of_result)
# out_df = data.frame(t(mapply(result_row, true_indicies)))

# submission_filename = "submission.csv"
# sink(submission_filename)
# cat("Id,")
# sink()
# write.table(out_df, submission_filename, append=T, sep=",", quote=F,
#             col.names=OUT_COL_NAMES,
#             row.names=seq(0, length(ys)-1))
