import json
import sys

ALL_WORDS = {}

def sentiments(afinnfile):
    scores = {}
    for line in afinnfile:
        term, score  = line.split("\t")
        scores[term] = int(score)
    return scores
    
def process_tweet_text(text, word_scores):
    words = text.split()
    whole_sentiment = sum(word_scores.get(word, 0) for word in words)
    unknown_words   = [w for w in words if w not in word_scores]
    for uw in unknown_words:
        current = ALL_WORDS.setdefault(uw, 0)
        ALL_WORDS[uw] = current + whole_sentiment
    
def main():
    word_scores  = sentiments(open(sys.argv[1]))
    tweet_file   = open(sys.argv[2])
    whole_tweets = [json.loads(line) for line in tweet_file]
        
    for wt in whole_tweets:
        if 'text' in wt.keys():
            process_tweet_text(wt['text'], word_scores)
            
    for k, v in ALL_WORDS.iteritems():
        print k, float(v)
    
if __name__ == '__main__':
    main()
