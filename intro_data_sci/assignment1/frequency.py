import collections
import json
import sys

def main():
    tweet_file = open(sys.argv[1])
    terms = {}
    
    whole_tweets = [json.loads(line) for line in tweet_file]
        
    for wt in whole_tweets:
        if 'text' in wt.keys():
            words = wt['text'].split()
            for w in words:
                count = terms.setdefault(w, 0)
                terms[w] = count + 1
    
    total_terms = sum(terms.values())
    for k, v in terms.iteritems():
        print k, float(v)/total_terms

if __name__ == '__main__':
    main()
