import collections
import json
import sys

def main():
    tweet_file   = open(sys.argv[1])    
    whole_tweets = [json.loads(line) for line in tweet_file]
    hashtags = []
    
    for wt in whole_tweets:
        if 'entities' in wt.keys():
            ents = wt['entities']
            if 'hashtags' in ents.keys():
                hashtags.extend(h['text'] for h in ents['hashtags'])
                
    for h, n in collections.Counter(hashtags).most_common(10):
        print h, n
            
if __name__ == '__main__':
    main()
