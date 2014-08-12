import json
import sys

def is_state(word):
    states = ['WA', 'WI', 'WV', 'FL', 'WY', 'NH', 'NJ', 'NM', 'NA', 
              'NC', 'ND', 'NE', 'NY', 'RI', 'NV', 'GU', 'CO', 'CA', 
              'GA', 'CT', 'OK', 'OH', 'KS', 'SC', 'KY', 'OR', 'SD', 
              'DE', 'DC', 'HI', 'PR', 'TX', 'LA', 'TN', 'PA', 'VA', 
              'VI', 'AK', 'AL', 'AS', 'AR', 'VT', 'IL', 'IN', 'IA', 
              'AZ', 'ID', 'ME', 'MD', 'MA', 'UT', 'MO', 'MN', 'MI', 
              'MT', 'MP', 'MS']
    return word in states
    
def sentiments(afinnfile):
    scores = {}
    for line in afinnfile:
        term, score  = line.split("\t")
        scores[term] = int(score)
    return scores

def location(tw_json):
    try:
        if tw_json is None:
            return 
            
        # tweet specific
        loc = (tw_json.get('place') or {}).get('full_name')
        if loc:
            return loc.strip().split()[-1].upper()
        
        # user specific
        loc = (tw_json.get('user') or {}).get('location')
        if loc:
            return loc.strip().split()[-1].upper()
    except:
        pass
        
def main():
    tweet_file   = open(sys.argv[2])
    whole_tweets = []
    word_scores  = sentiments(open(sys.argv[1]))
    whole_tweets = [json.loads(line) for line in tweet_file]
    totals = {}
    
    for wt in whole_tweets:
        if 'text' in wt.keys():
            loc = location(wt)
            if is_state(loc):
                words = wt['text'].split()
                tweet_score = sum(word_scores.get(word.lower(), 0) 
                                  for word in words)
                current = totals.get(loc) or []
                current.append(tweet_score)
                totals[loc] = current
        
    averages = [(t, float(sum(totals[t])) / len(totals[t]))
                for t in totals]

    max_state = averages[0][0]
    max_value = averages[0][1]
    for s, v in averages:
        if v > max_value:
            max_state = s
            max_value = v
            
    print max_state

if __name__ == '__main__':
    main()
