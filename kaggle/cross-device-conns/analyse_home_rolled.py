import pandas as pd

from collections import Counter


class Homogeneity(object):

    SAME = 1    # eg "b b b b"
    MIX  = 2    # eg "a b a a"
    DIFF = 3    # eg "a b c d"

    @staticmethod
    def categorise(ul):
        if len(ul) == len(set(ul)):
            return DIFF
        if len(set(ul)) == 1:
            return SAME
        return MIX

    @staticmethod
    def strength(ul):
        cat = Homogeneity.categorise(ul)
        if cat in (DIFF, SAME):
            return len(ul)
        most_common_freq = Counter(ul).most_common()[0][1]
        return len(ul) - most_common_freq


train = pd.DataFrame.from_csv('dev_train_basic.csv', index_col=False)

indicies = {'drawbridge_handle', 'device_id'}
categories = {'device_type',  'device_os',    'country',     'anonymous_c0', 
              'anonymous_c1', 'anonymous_c2', 'anonymous_5', 'anonymous_6', 
              'anonymous_7'}

# country
# device_os
# 

# X = train.ix[:,1:]       # variables
# y = train.ix[:,0]        # dependent variable

handles = train.ix[:,0]

category_similarities = {}
category_strengths = {}

# determine which of the variables should be the same or expect to be different

for h in set(handles):
    same_ids = train[train['drawbridge_handle'] == h]
    for s in same_ids:
        if s in categories and len(same_ids) > 1:
            valid_cats = [x for x in (same_ids[s]) if x != -1]
            similarity = Homogeneity.categorise(valid_cats)
            strength = Homogeneity.strength(valid_cats)
            category_similarities.setdefault(s, list()).append(similarity)
            category_strengths.setdefault(s, list()).append(strength)

    # if len(category_similarities) > 10:
    #     break



