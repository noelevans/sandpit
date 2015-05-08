import json
import pprint
import urllib2

def feed(username):
    template = 'https://api.twitter.com/1/statuses/user_timeline.json?' + \
               'include_entities=false&include_rts=true&screen_name=%s&count=50'
    url    = template % username
    output = urllib2.urlopen(url)
    html   = ''.join(output.readlines())
    tweets = json.loads(html)
    return list(reversed(map(lambda t : t['text'], tweets)))
    
if __name__ == '__main__':
    result = feed('noelevans')
    pprint.pprint(result)
