import json
import sys

def sentiments(afinnfile):
    scores = {}
    for line in afinnfile:
        term, score  = line.split("\t")
        scores[term] = int(score)
    return scores

def main():
    tweet_file   = open(sys.argv[2])
    whole_tweets = []
    word_scores  = sentiments(open(sys.argv[1]))
    
    for line in tweet_file:
        whole_tweets.append(json.loads(line))
        
    for wt in whole_tweets:
        if 'text' in wt.keys():
            words = wt['text'].split()
            print sum(word_scores.get(word, 0) for word in words)
        else:
            print 0

if __name__ == '__main__':
    main()
